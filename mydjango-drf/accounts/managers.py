from django.contrib.auth.base_user import BaseUserManager


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
