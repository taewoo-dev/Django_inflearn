from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User


class TokenService:
    @staticmethod
    def generate_jwt_token(user: User) -> tuple[str, str]:
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        return str(access), str(refresh)

    @staticmethod
    def blacklist_refresh_token(refresh_token: str) -> None:
        token = RefreshToken(refresh_token)
        token.blacklist()
