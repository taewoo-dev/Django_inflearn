import requests
from django.conf import settings

from accounts.constants import (
    NAVER_CALLBACK_URL,
    NAVER_STATE,
    NAVER_SCOPE,
    NAVER_LOGIN_URL,
    NAVER_TOKEN_URL,
    NAVER_PROFILE_URL,
)
from accounts.services.social_login_service import SocialLoginService


class NaverSocialLoginService(SocialLoginService):

    _client_id: str = settings.NAVER_CLIENT_ID
    _secret_id: str = settings.NAVER_SECRET
    _callback_url: str = NAVER_CALLBACK_URL
    _state: str = NAVER_STATE
    _scope: str = NAVER_SCOPE
    _login_url: str = NAVER_LOGIN_URL
    _token_url: str = NAVER_TOKEN_URL
    _profile_url: str = NAVER_PROFILE_URL

    def get_access_token(self, code: str, state: str) -> str:

        params = self._generate_access_token_payload(code, state)

        response = requests.get(NAVER_TOKEN_URL, params=params)

        token_response = response.json()

        return token_response.get("access_token")

    def _generate_access_token_payload(self, code: str, state: str) -> dict:
        payload = {
            "grant_type": "authorization_code",
            "client_id": self._client_id,
            "client_secret": self._secret_id,
            "code": code,
            "state": state,
        }
        return payload
