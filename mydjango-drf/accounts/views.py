from django.contrib.auth import login, logout

from django.core.signing import SignatureExpired, BadSignature

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from accounts.serializers import UserRegistrationSerializer, UserLoginSerializer
from accounts.services.email_service import EmailService
from accounts.services.token_service import TokenService
from accounts.services.user_service import UserService


# 회원가입 API
class UserRegistrationAPIView(GenericAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    email_service = EmailService()
    user_service = UserService()

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        self.user_service.create_common_user_by_email(
            email=validated_data["email"],
            nickname=validated_data["nickname"],
            password=validated_data["password"],
        )

        email = validated_data.get("email")

        token = self.email_service.create_signed_email_token(email)
        subject, message = self.email_service.get_verification_email_content(token)
        self.email_service.send_email(subject, message, email)

        data = {
            "success": True,
            "nickname": validated_data["nickname"],
            "message": "User registered successfully.",
        }

        return Response(data, status=status.HTTP_201_CREATED)


# 이메일 인증 API
class VerifyEmailAPIView(APIView):
    permission_classes = [AllowAny]
    email_service = EmailService()
    user_service = UserService()

    def get(self, request: Request, *args, **kwargs) -> Response:
        token = request.GET.get("token", "")

        try:
            email = self.email_service.validate_email_token(token=token)
            self.user_service.activate_user_by_email(email=email)
            return Response(
                {"message": "Email verified successfully."}, status=status.HTTP_200_OK
            )
        except (BadSignature, SignatureExpired):
            return Response(
                {"error": "Invalid or expired token."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except User.DoesNotExist:
            return Response(
                {"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND
            )


# 로그인 API
class UserLoginAPIView(GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]
    token_service = TokenService()

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]

            login(request, user)
            access, refresh = self.token_service.generate_jwt_token(user)

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

        logout(request)

        if refresh_token:
            token_service = TokenService()
            token_service.blacklist_refresh_token(refresh_token)

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
