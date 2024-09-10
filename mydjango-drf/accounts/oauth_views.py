# Oauth Naver 로그인 API
from urllib.parse import urlencode

import requests
from django.contrib.auth import login
from django.core import signing
from django.views.generic import RedirectView
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from accounts.models import User
from accounts.oauth_serializer import NaverCallBackSerializer
from config import settings

NAVER_CALLBACK_URL = "/accounts/naver/callback/"
NAVER_STATE = "naver_login"
NAVER_LOGIN_URL = "https://nid.naver.com/oauth2.0/authorize"
NAVER_TOKEN_URL = "https://nid.naver.com/oauth2.0/token"
NAVER_PROFILE_URL = "https://openapi.naver.com/v1/nid/me"


# NaverRedirectAPIView
class NaverLoginRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        domain = self.request.scheme + "://" + self.request.META.get("HTTP_HOST", "")
        callback_url = domain + NAVER_CALLBACK_URL
        state = signing.dumps(NAVER_STATE)
        print(callback_url)
        params = {
            "response_type": "code",
            "client_id": settings.NAVER_CLIENT_ID,
            "redirect_uri": callback_url,
            "state": state,
        }
        return f"{NAVER_LOGIN_URL}?{urlencode(params)}"


class NaverCallBackView(GenericAPIView):
    serializer_class = NaverCallBackSerializer
    permission_classes = [AllowAny]

    def get(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        code = validated_data.get("code")
        state = validated_data.get("state")

        params = {
            "grant_type": "authorization_code",
            "client_id": settings.NAVER_CLIENT_ID,
            "client_secret": settings.NAVER_SECRET,
            "code": code,
            "state": state,
        }

        response = requests.get(NAVER_TOKEN_URL, params=params)
        result = response.json()

        access_token = result.get("access_token")

        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        response = requests.get(NAVER_PROFILE_URL, headers=headers)

        if response.status_code != 200:
            return Response(
                {"error": "User Not Found"}, status=status.HTTP_404_NOT_FOUND
            )

        result = response.json()

        email = result.get("response").get("email")

        user = User.objects.get(email=email)
        if user:
            if not user.is_active:
                user.is_active = True
                user.save()
            login(request, user)
            return Response(
                {"message": "successful Naver Login"}, status=status.HTTP_200_OK
            )
