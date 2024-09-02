from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict

from .mixins import JsonResponseMixin
from .models import Post
from .serializers import PostSerializer, PostListSerializer, PostDetailSerializer


# @api_view(["GET"])
# def post_list(request: Request) -> Response:
#     # post_list에서 외래키 참조에 대한 n+1 문제 발생 -> select_related를 이용하여 즉시 가져오기
#     post_qs = Post.objects.all().select_related("author")
#
#     serializer = PostListSerializer(instance=post_qs, many=True)
#     list_data: ReturnList = serializer.data
#     return Response(list_data)


# JsonResponse(post_qs, safe=False) 장고 기본에서는 qs객체 지원 x -> 리스트로 변환


class PostListAPIView(JsonResponseMixin, ListAPIView):
    queryset = PostListSerializer.get_optimized_queryset()
    serializer_class = PostListSerializer


post_list = PostListAPIView.as_view()


# @api_view(["GET"])
# def post_detail(request: Request, pk: int) -> Response:
#     post = get_object_or_404(Post, pk=pk)
#     serialize = PostDetailSerializer(instance=post)
#     detail_data: ReturnDict = serialize.data
#
#     return Response(detail_data)


class PostDetailAPIView(JsonResponseMixin, RetrieveAPIView):
    queryset = PostDetailSerializer.get_optimized_queryset()
    serializer_class = PostDetailSerializer


post_detail = PostDetailAPIView.as_view()
