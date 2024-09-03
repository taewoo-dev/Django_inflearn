from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict

from .mixins import JsonResponseMixin, PermissionDebugMixin
from .models import Post
from .permissions import IsAuthorOrReadonly
from .serializers import PostSerializer, PostListSerializer, PostDetailSerializer


class PostListAPIView(JsonResponseMixin, PermissionDebugMixin, ListAPIView):
    queryset = PostListSerializer.get_optimized_queryset()
    serializer_class = PostListSerializer


post_list = PostListAPIView.as_view()


class PostRetrieveAPIView(JsonResponseMixin, PermissionDebugMixin, RetrieveAPIView):
    queryset = PostDetailSerializer.get_optimized_queryset()
    serializer_class = PostDetailSerializer


post_detail = PostRetrieveAPIView.as_view()


class PostCreateAPIView(PermissionDebugMixin, CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadonly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


post_new = PostCreateAPIView().as_view()


class PostUpdateAPIView(PermissionDebugMixin, UpdateAPIView):
    queryset = PostSerializer.get_optimized_queryset()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadonly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


post_edit = PostUpdateAPIView.as_view()


class PostDestroyAPIView(PermissionDebugMixin, DestroyAPIView):
    queryset = PostSerializer.get_optimized_queryset()
    permission_classes = [IsAuthorOrReadonly]


post_delete = PostDestroyAPIView.as_view()
