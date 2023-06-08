from api.filters import TitleFilter
from api.permissions import AdminOrReadOnly, isUserAdminModeratorOrReadOnly
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitlePostSerializer, TitleReadSerializer,
                             ReviewSerializer, CommentSerializer)
from .pagination import PageNumberPagination
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from reviews.models import Category, Genre, Title, Review


class LimitPutRequest(viewsets.ModelViewSet):
    http_method_names = (
        "get",
        "post",
        "patch",
        "delete",
    )


class TitleViewSet(LimitPutRequest):
    queryset = Title.objects.annotate(rating=Avg("reviews__score")).order_by("id")
    serializer_class = TitleReadSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return TitleReadSerializer
        return TitlePostSerializer


class BaseListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class GenreViewSet(BaseListCreateDestroyViewSet):
    """
    Получить список всех жанров. Права доступа: Доступно без токена
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(BaseListCreateDestroyViewSet):
    """
    Получить список всех категорий. Права доступа: Доступно без токена
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Для модели отзыва."""
    serializer_class = ReviewSerializer
    permission_classes = (isUserAdminModeratorOrReadOnly, )
    pagination_class = PageNumberPagination

    def get_title(self):
        return get_object_or_404(
            Title,
            id=self.kwargs.get("title_id")
        )

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title_id=self.get_title().id
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Для модели комментариев."""
    serializer_class = CommentSerializer
    permission_classes = (isUserAdminModeratorOrReadOnly, )
    pagination_class = PageNumberPagination

    def get_review(self):
        return get_object_or_404(
            Review,
            id=self.kwargs.get("review_id"),
            title_id=self.kwargs.get("title_id")
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review_id=self.get_review().id
        )
