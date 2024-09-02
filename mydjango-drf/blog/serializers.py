from django.db.models import QuerySet

from rest_framework import serializers
from .models import Post, User, Comment


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ["id", "title", "content"]


class AuthorSerializer(serializers.ModelSerializer):
    # serializer의 매서드 필드는 default로 get_fieldname을 찾아서 자동호출하여 field를 만든다
    name = serializers.SerializerMethodField()

    def get_name(self, user) -> str:
        return f"{user.last_name}{user.first_name}".strip()

    class Meta:
        model = User
        fields = ["id", "username", "email", "name"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "message"]


class PostListSerializer(serializers.ModelSerializer):
    # 1) 참조하는 모델을 문자열로 반환하여 사용하는 방법
    # author = serializers.StringRelatedField()
    # 2) 참조하는 모델을 직접 정해서 사용하는 방법, 모델의 필드명과 다르게 설정할 수 있다
    # author = serializers.CharField(source="author.username")
    # 3) author에 대한 serializer를 만들기
    author = AuthorSerializer()

    class Meta:
        model = Post
        fields = ["id", "title", "author"]

    @staticmethod
    def get_optimized_queryset() -> QuerySet[Post]:
        return Post.objects.all().only("id", "title", "author").select_related("author")


class PostDetailSerializer(serializers.ModelSerializer):
    # author = serializers.StringRelatedField()
    # author = serializers.CharField(source="author.username")
    author = AuthorSerializer()

    # 1) 참조하는 모델을 문자열로 반환하여 사용하는 방법
    # comment_set : Post와 Comment 두 모델간의 related name을 따로 설정을 안해뒀기에 comment_set 변수명이 default
    # comment model은 모델에서 문자열 반환시 message필드가 출력되게 설정되어있다.
    # comment_list = serializers.StringRelatedField(source="comment_set", many=True)

    # 2) comment에 대한 serializer를 만들기
    comment_list = CommentSerializer(source="comment_set", many=True)

    class Meta:
        model = Post
        fields = ["id", "title", "content", "author", "comment_list"]

    @staticmethod
    def get_optimized_queryset() -> QuerySet[Post]:
        return Post.objects.all()
