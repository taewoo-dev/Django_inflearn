from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView

from accounts.serializers import UserRegistrationSerializer


class UserRegistrationAPIView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = []
    pass


class UserLoginAPIView(APIView):
    pass
