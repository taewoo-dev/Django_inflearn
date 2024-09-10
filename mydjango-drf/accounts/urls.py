from django.urls import path, include
from .oauth_views import (
    NaverLoginRedirectView,
    NaverCallBackView,
    KakaoLoginRedirectView,
    KakaoCallBackView,
    GoogleLoginRedirectView,
    GoogleCallBackView,
)
from .views import (
    UserRegistrationAPIView,
    PasswordChangeAPIView,
    PasswordResetAPIView,
    UserDetailAPIView,
    UserListAPIView,
    UserDeactivationAPIView,
    UserTokenAPIView,
    UserLogoutAPIView,
    UserLoginAPIView,
    VerifyEmailAPIView,
)

urlpatterns = [
    path(
        "register/", UserRegistrationAPIView.as_view(), name="user-register"
    ),  # 회원가입
    path("verify/", VerifyEmailAPIView.as_view(), name="verfiy-email"),  # 이메일 인증
    path("login/", UserLoginAPIView.as_view(), name="user-login"),  # 로그인
    path("logout/", UserLogoutAPIView.as_view(), name="user-logout"),  # 로그아웃
    # simple JWT
    # path("login/simpleJWT", TokenObtainPairView.as_view()),
    # path("login/simpleJWT/refresh", TokenRefreshView.as_view()),
    # path("login/simpleJWT/verify", TokenVerifyView.as_view()),
    # path('password-change/', PasswordChangeAPIView.as_view(), name='password-change'),  # 비밀번호 변경
    # path('password-reset/', PasswordResetAPIView.as_view(), name='password-reset'),  # 비밀번호 초기화
    # path('profile/', UserDetailAPIView.as_view(), name='user-detail'),  # 유저 프로필 조회 및 수정
    # path('users/', UserListAPIView.as_view(), name='user-list'),  # 유저 목록 조회 (관리자)
    # path('deactivate/', UserDeactivationAPIView.as_view(), name='user-deactivate'),  # 유저 비활성화
    # path('token/', UserTokenAPIView.as_view(), name='user-token'),  # JWT 토큰 생성
    # Oauth url
    path(
        "naver/login", NaverLoginRedirectView.as_view(), name="naver-login"
    ),  # Naver Login
    path(
        "naver/callback/", NaverCallBackView.as_view(), name="naver-callback"
    ),  # Naver Callback
    path(
        "kakao/login", KakaoLoginRedirectView.as_view(), name="kakao-login"
    ),  # Kakao Login
    path(
        "kakao/callback/", KakaoCallBackView.as_view(), name="naver-callback"
    ),  # KaKao Callback
    path(
        "google/login", GoogleLoginRedirectView.as_view(), name="google-login"
    ),  # Google Login
    path(
        "google/callback/", GoogleCallBackView.as_view(), name="google-callback"
    ),  # Google Callback
]
