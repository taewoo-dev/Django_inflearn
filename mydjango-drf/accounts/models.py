from typing import Optional

from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.managers import UserManger


# Create your models here.


class User(AbstractUser):
    username = None  # username 필드를 제거
    email = models.EmailField(
        verbose_name="email",
        unique=True,
    )
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    nickname = models.CharField(
        "nickname", max_length=20, unique=True, null=True, blank=True
    )

    objects = UserManger()
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "유저"
        verbose_name_plural = f"{verbose_name} 목록"

    def get_short_name(self):
        return self.nickname

    def get_full_name(self):
        return self.nickname

    def __str__(self):
        return self.nickname or self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin

    @classmethod
    def activate_user_by_email(cls, email: str) -> None:
        user = cls.objects.get(email=email)
        user.is_active = True
        user.save()

    @classmethod
    def get_user_by_email(cls, email: str) -> Optional["User"]:
        try:
            return cls.objects.get(email=email)
        except cls.DoesNotExist:
            return None
