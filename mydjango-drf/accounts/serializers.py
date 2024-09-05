from django.db.models import QuerySet
from rest_framework import serializers

from blog.mixins import PermissionDebugMixin
from .models import User


# 회원가입 serializer
class UserRegistrationSerializer(PermissionDebugMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "nickname", "password", "password2"]


# 로그인 serializer
class UserLoginSerializer(serializers.Serializer):
    pass


# 사용자 비밀번호 변경 serializer
class PasswordChangeSerializer(serializers.Serializer):
    pass


# 사용자 비밀번호 초기화 serializer
class PasswordResetSerializer(serializers.Serializer):
    pass


# 유저 프로필 조회 및 수정을 위한 serializer
class UserDetailSerializer(serializers.ModelSerializer):
    pass


# 관리자 또는 사용자에게 유저 목록을 제공하는 serializer
class UserListSerializer(serializers.ModelSerializer):
    pass


# 유저 계정을 비활성화하는 serializer
class UserDeactivationSerializer(serializers.ModelSerializer):
    pass


# 유저의 로그인 후 토큰을 발급하는 serializer
class UserTokenSerializer(serializers.Serializer):
    pass
