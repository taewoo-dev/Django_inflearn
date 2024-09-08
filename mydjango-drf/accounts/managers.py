from typing import Optional, Tuple

from django.contrib.auth.base_user import BaseUserManager
from rest_framework.request import Request

from accounts.models import User
from accounts.services import LoginService, LogoutService, TokenService, EmailService


class UserManger(BaseUserManager):
    def create_user(self, email, password, nickname):
        if not email:
            raise ValueError("올바른 메세지를 입력해주세요")
        user = self.model(
            email=self.normalize_email(email),
        )
        user.nickname = nickname
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, nickname="관리자"):
        user = self.create_user(email=email, password=password, nickname=nickname)
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class AuthenticationManager:
    login_service = LoginService()
    logout_service = LogoutService()
    token_service = TokenService()
    email_service = EmailService()

    def login(self, request: Request, user: User) -> None:
        self.login_service.perform_login(request, user)

    def logout(self, request: Request, refresh_token: Optional[str] = None) -> None:
        self.logout_service.perform_logout(request)

        if refresh_token:
            self.token_service.blacklist_refresh_token(refresh_token)

    def get_token(self, user: User) -> Tuple[str, str]:
        return self.token_service.generate_jwt_token(user)
