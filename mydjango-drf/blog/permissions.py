# core/permissions.py

from django.db.models import Model
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        # 조회 API에 대해서는 True 반환
        if request.method in permissions.SAFE_METHODS:
            return True
        # 그 외에 생성, 수정, 삭제 API에 대해서는 권한 확인
        return request.user.is_authenticated

    # 2차 필터
    def has_object_permission(
        self, request: Request, view: APIView, obj: Model
    ) -> bool:
        # 조회 API에 대해서는 참을 반환
        if request.method in permissions.SAFE_METHODS:
            return True

        # 삭제는 관리자만 가능
        # if request.method == "DELETE":
        #     return request.user.is_staff

        if not hasattr(obj, "author"):  # author 필드가 있다면, 레코드 조회 수행
            return False

        return obj.author == request.user  # author 와 유저가 같은지 확인
