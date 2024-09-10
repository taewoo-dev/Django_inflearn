from django.core import signing
from rest_framework import serializers

NAVER_STATE = "naver_login"


class NaverCallBackSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    state = serializers.CharField(required=True)

    def validate_state(self, state: str) -> str:
        if NAVER_STATE != signing.loads(state):
            raise serializers.ValidationError("잘못된 state 값이 들어왔습니다")
        return state
