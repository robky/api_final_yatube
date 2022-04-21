# TODO:  Напишите свой вариант
from rest_framework import viewsets, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from posts.models import Group, Post
from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, IsAuthor)

    def get_post(self):
        post_id = self.kwargs.get("post_id")
        return get_object_or_404(Post, id=post_id)

    def get_queryset(self):
        post = self.get_post()
        return post.comments

    def perform_create(self, serializer):
        post = self.get_post()
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
