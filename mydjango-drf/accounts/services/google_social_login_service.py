import requests
from django.conf import settings

from accounts.constants import (
    GOOGLE_CALLBACK_URL,
    GOOGLE_STATE,
    GOOGLE_SCOPE,
    GOOGLE_LOGIN_URL,
    GOOGLE_PROFILE_URL,
    GOOGLE_TOKEN_URL,
)
from accounts.services.social_login_service import SocialLoginService


class GoogleSocialLoginService(SocialLoginService):

    _client_id: str = settings.GOOGLE_CLIENT_ID
    _secret_id: str = settings.GOOGLE_SECRET
    _callback_url: str = GOOGLE_CALLBACK_URL
    _state: str = GOOGLE_STATE
    _scope: str = GOOGLE_SCOPE
    _login_url: str = GOOGLE_LOGIN_URL
    _token_url: str = GOOGLE_TOKEN_URL
    _profile_url: str = GOOGLE_PROFILE_URL

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
