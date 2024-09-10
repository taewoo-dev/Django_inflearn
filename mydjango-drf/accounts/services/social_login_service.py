from abc import ABC, abstractmethod
from urllib.parse import urlencode

import requests
from django.core import signing


class SocialLoginService(ABC):

    _client_id: str
    _secret_id: str
    _callback_url: str
    _state: str
    _scope: str
    _login_url: str
    _token_url: str
    _profile_url: str

    @property
    def signed_state(self):
        return signing.dumps(self._state)

    def generate_login_url(self) -> str:
        params = self._generate_login_params()
        return self._create_login_url(params)

    def _generate_login_params(self) -> dict:
        return {
            "response_type": "code",
            "client_id": self._client_id,
            "redirect_uri": self._callback_url,
            "state": self.signed_state,
            "scope": self._scope,
        }

    def _create_login_url(self, params: dict) -> str:
        return f"{self._login_url}?{urlencode(params)}"

    @abstractmethod
    def get_access_token(self, *args, **kwargs):
        pass

    @abstractmethod
    def _generate_access_token_payload(self, *args, **kwargs):
        pass

    def get_profile_json(self, access_token: str) -> dict:
        headers = self._generate_auth_headers(access_token)

        response = requests.get(self._profile_url, headers=headers)

        return response.json()

    def _generate_auth_headers(self, access_token: str) -> dict:
        headers = {
            "Authorization": f"Bearer {access_token}",
        }
        return headers
