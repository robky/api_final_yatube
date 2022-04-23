# TODO:  Напишите свой вариант
from django.shortcuts import get_list_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from posts.models import Follow, Group, Post, User
from .serializers import (CommentSerializer, FollowSerializer,
                          GroupSerializer, PostSerializer)
from .permissions import FollowsPermission, OwnerOrReadOnly, ReadOnly


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (OwnerOrReadOnly, )

    def get_post(self):
        post_id = self.kwargs.get("post_id")
        return get_object_or_404(Post, id=post_id)

    def get_queryset(self):
        post = self.get_post()
        return post.comments

    def perform_create(self, serializer):
        post = self.get_post()
        serializer.save(author=self.request.user, post=post)

    def get_permissions(self):
        # Если в GET-запросе требуется получить информацию об объекте
        if self.action == 'retrieve':
            # Вернем обновленный перечень используемых пермишенов
            return (ReadOnly(),)
        # Для остальных ситуаций оставим текущий перечень пермишенов без
        # изменений
        return super().get_permissions()


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (FollowsPermission, IsAuthenticated)

    def get_queryset(self):
        return get_list_or_404(Follow, user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        following_name = serializer.initial_data.get('following')
        following = get_object_or_404(
            User,
            username=following_name
        )
        if user == following:
            raise ValidationError([f"Подписка на самого себя невозможна."])
        if Follow.objects.filter(user=user, following=following).count():
            raise ValidationError([f"Уже подписан на автора "
                                   f"'{following_name}'."])
        serializer.save(user=user, following=following)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (OwnerOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_permissions(self):
        # Если в GET-запросе требуется получить информацию об объекте
        if self.action == 'retrieve':
            # Вернем обновленный перечень используемых пермишенов
            return (ReadOnly(),)
        # Для остальных ситуаций оставим текущий перечень пермишенов без
        # изменений
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
