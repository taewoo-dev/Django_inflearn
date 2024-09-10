from django.contrib.auth import login

from django.views.generic import RedirectView
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from accounts.models import User
from accounts.oauth_serializer import (
    NaverCallBackSerializer,
    KakaoCallBackSerializer,
    GoogleCallBackSerializer,
)
from accounts.services.google_social_login_service import GoogleSocialLoginService
from accounts.services.kakao_social_login_service import KakaoSocialLoginService
from accounts.services.naver_social_login_service import NaverSocialLoginService


# NaverRedirectAPIView 로그인 창으로 redirect
class NaverLoginRedirectView(RedirectView):
    social_service = NaverSocialLoginService()

    def get_redirect_url(self, *args, **kwargs) -> str:
        return self.social_service.generate_login_url()


# NaverCallBackAPIView 로그인 and 회원가입
class NaverCallBackView(GenericAPIView):
    serializer_class = NaverCallBackSerializer
    permission_classes = [AllowAny]
    social_service = NaverSocialLoginService()

    def get(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        code = validated_data.get("code")
        state = validated_data.get("state")

        access_token = self.social_service.get_access_token(code, state)
        profile_response = self.social_service.get_profile_json(access_token)
        profile_data = profile_response.get("response")
        email = profile_data.get("email")

        user = self.social_service.handle_user_by_email(email)

        if user:
            login(request, user)
            return Response({"message": "successful Login"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "User could not be created"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# KakaoRedirectAPIView 로그인 창으로 redirect
class KakaoLoginRedirectView(RedirectView):
    social_service = KakaoSocialLoginService()

    def get_redirect_url(self, *args, **kwargs) -> str:
        return self.social_service.generate_login_url()


# KakaoCallBackAPIView 로그인 and 회원가입
class KakaoCallBackView(GenericAPIView):
    serializer_class = KakaoCallBackSerializer
    permission_classes = [AllowAny]
    social_service = KakaoSocialLoginService()

    def get(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        code = validated_data.get("code")

        access_token = self.social_service.get_access_token(code)
        profile_response = self.social_service.get_profile_json(access_token)
        user_data = profile_response.get("kakao_account")
        email = user_data.get("email")

        user = self.social_service.handle_user_by_email(email)

        if user:
            login(request, user)
            return Response({"message": "successful Login"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "User could not be created"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# GoogleRedirectAPIView 로그인 창으로 redirect
class GoogleLoginRedirectView(RedirectView):
    social_service = GoogleSocialLoginService()

    def get_redirect_url(self, *args, **kwargs) -> str:
        return self.social_service.generate_login_url()


# GoogleCallBackAPIView 로그인 and 회원가입
class GoogleCallBackView(GenericAPIView):
    serializer_class = GoogleCallBackSerializer
    permission_classes = [AllowAny]
    social_service = GoogleSocialLoginService()

    def get(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        code = validated_data.get("code")

        access_token = self.social_service.get_access_token(code)
        profile_response = self.social_service.get_profile_json(access_token)
        email = profile_response.get("email")

        user = self.social_service.handle_user_by_email(email)

        if user:
            login(request, user)
            return Response({"message": "successful Login"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "User could not be created"},
                status=status.HTTP_400_BAD_REQUEST,
            )
