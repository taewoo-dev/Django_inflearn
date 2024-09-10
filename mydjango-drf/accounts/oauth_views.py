from django.contrib.auth import login

from django.views.generic import RedirectView
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from accounts.models import User
from accounts.oauth_serializer import NaverCallBackSerializer
from accounts.services import NaverSocialLoginService


# NaverRedirectAPIView 로그인 창으로 redirect
class NaverLoginRedirectView(RedirectView):
    social_service = NaverSocialLoginService()

    def get_redirect_url(self, *args, **kwargs) -> str:
        domain = self.request.scheme + "://" + self.request.META.get("HTTP_HOST", "")

        login_url = self.social_service.generate_naver_login_url(domain=domain)

        return login_url


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

        access_token = self.social_service.get_naver_access_token(code, state)

        # 요청에 대한 응답이 잘못되었을 경우에 대한 예외처리
        # if access_token == None:
        #     return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        profile_response = self.social_service.get_naver_profile(access_token)

        email = profile_response.get("email")

        user = User.get_user_by_email(email=email)

        # 해당 email의 유저가 이미 있는 경우
        if user:
            if not user.is_active:
                user.is_active = True
                user.save()
            login(request, user)
            return Response(
                {"message": "successful Naver Login"}, status=status.HTTP_200_OK
            )

        # 새로운 유저 생성, nickname 설정 api는 따로 설계,
        user = User.objects.create_social_user(email=email)
        login(request, user)

        return Response(
            {"message": "successful Sign up and Login !!"},
            status=status.HTTP_201_CREATED,
        )
