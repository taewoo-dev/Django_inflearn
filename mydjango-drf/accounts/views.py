from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from accounts.serializers import UserRegistrationSerializer, UserLoginSerializer


# 회원가입 API
class UserRegistrationAPIView(GenericAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        user = User.objects.create_user(
            email=validated_data["email"],
            nickname=validated_data["nickname"],
            password=validated_data["password"],
        )

        return Response(
            {"message": "User registered successfully."}, status=status.HTTP_201_CREATED
        )


# session 로그인 API
class UserSessionLoginAPIView(GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]
            login(request, user)
            # JWT 토큰 생성
            access, refresh = self.get_jwt_token(user)
            return Response(
                {
                    "message": "Login successful",
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "nickname": user.nickname,
                    },
                    "refresh": str(refresh),
                    "access": str(access),
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        return access, refresh


# session 로그아웃 API
class UserSessionLogoutAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)


# jwt 로그인 API
class UserJwtLoginAPIView(GenericAPIView):
    pass


# jwt 로그아웃 API
class UserJwtLogoutView(GenericAPIView):
    pass


# 비밀번호 API
class PasswordChangeAPIView:
    pass


class PasswordResetAPIView:
    pass


class UserDetailAPIView:
    pass


class UserListAPIView:
    pass


class UserDeactivationAPIView:
    pass


class UserTokenAPIView:
    pass
