import requests

from accounts.constants import (
    KAKAO_CALLBACK_URL,
    KAKAO_STATE,
    KAKAO_SCOPE,
    KAKAO_LOGIN_URL,
    KAKAO_TOKEN_URL,
    KAKAO_PROFILE_URL,
)
from accounts.services.social_login_service import SocialLoginService
from django.conf import settings


class KakaoSocialLoginService(SocialLoginService):

    _client_id: str = settings.KAKAO_CLIENT_ID
    _secret_id: str = settings.KAKAO_SECRET
    _callback_url: str = KAKAO_CALLBACK_URL
    _state: str = KAKAO_STATE
    _scope: str = KAKAO_SCOPE
    _login_url: str = KAKAO_LOGIN_URL
    _token_url: str = KAKAO_TOKEN_URL
    _profile_url: str = KAKAO_PROFILE_URL

    def get_access_token(self, code: str) -> str:

        payload = self._generate_access_token_payload(code)

        response = requests.post(self._token_url, data=payload)

        token_response = response.json()

        return token_response.get("access_token")

    def _generate_access_token_payload(self, code: str) -> dict:
        payload = {
            "grant_type": "authorization_code",
            "client_id": self._client_id,
            "client_secret": self._secret_id,
            "code": code,
            "redirect_uri": self._callback_url,
        }
        return payload
