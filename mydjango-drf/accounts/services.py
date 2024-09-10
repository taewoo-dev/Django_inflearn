from typing import Tuple
from urllib.parse import urlencode

import requests
from django.conf import settings
from django.core import signing
from django.core.mail import send_mail
from django.core.signing import TimestampSigner

from rest_framework_simplejwt.tokens import RefreshToken

from accounts.constants import (
    NAVER_CALLBACK_URL,
    NAVER_STATE,
    NAVER_LOGIN_URL,
    NAVER_TOKEN_URL,
    NAVER_PROFILE_URL,
)
from accounts.models import User


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
    signer = TimestampSigner()

    def create_signed_email_token(self, email: str) -> str:
        signed_user_email = self.signer.sign(email)  # email: sign_data
        return signing.dumps(signed_user_email)  # 암호화

    def validate_email_token(self, token: str) -> str:
        decoded_user_email = signing.loads(token)
        return self.signer.unsign(decoded_user_email, max_age=60 * 10)

    @staticmethod
    def get_verification_email_content(
        scheme: str, meta: dict, token: str
    ) -> tuple[str, str]:
        url = f"{scheme}://{meta['HTTP_HOST']}/accounts/verify/?token={token}"
        subject = "이메일 인증을 완료해주세요"
        message = f"다음 링크를 클릭해 주세요. {url}"

        return subject, message

    @staticmethod
    def send_email(subject: str, message: str, to_email: str) -> None:
        to_email = to_email if isinstance(to_email, list) else [to_email]
        send_mail(subject, message, settings.EMAIL_HOST_USER, to_email)


class NaverSocialLoginService:
    def generate_naver_login_url(self, domain: str) -> str:
        callback_url, state = self._generate_login_params_elements(domain=domain)
        params = self._generate_naver_login_params(callback_url, state)
        url = self._create_naver_login_url(params)
        return url

    def _generate_login_params_elements(self, domain: str) -> tuple[str, str]:
        callback_url = domain + NAVER_CALLBACK_URL
        state = signing.dumps(NAVER_STATE)
        return callback_url, state

    def _generate_naver_login_params(self, callback_url: str, state: str) -> dict:
        return {
            "response_type": "code",
            "client_id": settings.NAVER_CLIENT_ID,
            "redirect_uri": callback_url,
            "state": state,
        }

    def _create_naver_login_url(self, params: dict) -> str:
        return f"{NAVER_LOGIN_URL}?{urlencode(params)}"

    def get_naver_access_token(self, code: str, state: str) -> str:
        params = self._generate_naver_access_token_params(code, state)
        response = requests.get(NAVER_TOKEN_URL, params=params)
        if response.status_code != 200:
            return
        token_response = response.json()

        return token_response.get("access_token")

    def _generate_naver_access_token_params(self, code: str, state: str) -> dict:
        params = {
            "grant_type": "authorization_code",
            "client_id": settings.NAVER_CLIENT_ID,
            "client_secret": settings.NAVER_SECRET,
            "code": code,
            "state": state,
        }
        return params

    def get_naver_profile(self, access_token: str) -> dict:
        headers = self._generate_auth_headers(access_token)

        response = requests.get(NAVER_PROFILE_URL, headers=headers)

        profile_response = response.json()

        return profile_response.get("response")

    def _generate_auth_headers(self, access_token: str) -> dict:
        headers = {
            "Authorization": f"Bearer {access_token}",
        }
        return headers
