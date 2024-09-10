from django.core import signing
from rest_framework import serializers

from accounts.constants import KAKAO_STATE, NAVER_STATE


class SocialCallBackSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    state = serializers.CharField(required=True)

    def get_expected_state(self) -> str:
        """
        social service에 맞는 state 설정
        """
        pass

    def validate_state(self, state: str) -> str:
        # 추상 메서드를 통해 기대하는 state 값을 가져옴
        expected_state = self.get_expected_state()
        if expected_state != signing.loads(state):
            raise serializers.ValidationError("잘못된 state 값이 들어왔습니다")
        return state


class NaverCallBackSerializer(SocialCallBackSerializer):
    def get_expected_state(self) -> str:
        # 네이버 전용 state 값 반환
        return NAVER_STATE


class KakaoCallBackSerializer(SocialCallBackSerializer):
    def get_expected_state(self) -> str:
        # 카카오 전용 state 값 반환
        return KAKAO_STATE
