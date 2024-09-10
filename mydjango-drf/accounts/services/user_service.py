from typing import Optional

from accounts.models import User


class UserService:

    @staticmethod
    def create_common_user_by_email(email: str, nickname: str, password: str) -> User:
        return User.objects.create_user(
            email=email, nickname=nickname, password=password
        )

    @staticmethod
    def activate_user(user: User) -> None:
        if not user.is_active:
            user.is_active = True
            user.save()

    def activate_user_by_email(self, email: str) -> None:
        user = User.get_user_by_email(email=email)
        if user:
            self.activate_user(user)

    def get_or_create_social_user_by_email(self, email: str) -> Optional[User]:
        user = User.get_user_by_email(email=email)
        if user:
            self.activate_user(user)
        else:
            user = User.objects.create_social_user(email=email)
        return user
