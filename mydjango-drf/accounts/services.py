from typing import Tuple

from django.contrib.auth import login, logout
from rest_framework.request import Request

from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User


class LoginService:
    @staticmethod
    def perform_login(request: Request, user: User) -> None:
        login(request, user)


class LogoutService:
    @staticmethod
    def perform_logout(request: Request) -> None:
        logout(request)


class TokenService:
    @staticmethod
    def generate_jwt_token(user: User) -> Tuple[str, str]:
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        return str(access), str(refresh)

    @staticmethod
    def blacklist_refresh_token(refresh_token: str) -> None:
        token = RefreshToken(refresh_token)
        token.blacklist()


class EmailService:
    pass
