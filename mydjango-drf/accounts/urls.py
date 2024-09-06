from django.urls import path, include
from . import views
from .api import (
    UserRegistrationAPIView,
    UserLoginAPIView,
    PasswordChangeAPIView,
    PasswordResetAPIView,
    UserDetailAPIView,
    UserListAPIView,
    UserDeactivationAPIView,
    UserTokenAPIView,
)

urlpatterns = [
    path(
        "register/", UserRegistrationAPIView.as_view(), name="user-register"
    ),  # 회원가입
    path("login/", UserLoginAPIView.as_view(), name="user-login"),  # 로그인
    # path('password-change/', PasswordChangeAPIView.as_view(), name='password-change'),  # 비밀번호 변경
    # path('password-reset/', PasswordResetAPIView.as_view(), name='password-reset'),  # 비밀번호 초기화
    # path('profile/', UserDetailAPIView.as_view(), name='user-detail'),  # 유저 프로필 조회 및 수정
    # path('users/', UserListAPIView.as_view(), name='user-list'),  # 유저 목록 조회 (관리자)
    # path('deactivate/', UserDeactivationAPIView.as_view(), name='user-deactivate'),  # 유저 비활성화
    # path('token/', UserTokenAPIView.as_view(), name='user-token'),  # JWT 토큰 생성
]
