from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from accounts.managers import AuthenticationManager
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


# 로그인 API
class UserLoginAPIView(GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]

            auth_manager = AuthenticationManager()
            auth_manager.login(request, user)
            access, refresh = auth_manager.get_token(user)

            return Response(
                {
                    "message": "Login successful",
                    "access": access,
                    "refresh": refresh,
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 로그아웃 API
class UserLogoutAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        refresh_token = request.data.get("refresh")

        auth_manager = AuthenticationManager()
        auth_manager.logout(refresh_token)

        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)


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
