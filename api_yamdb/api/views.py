from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets


from api.filters import TitleFilter
from api.permissions import (AdminOrReadOnly)
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitlePostSerializer, TitleReadSerializer)
from reviews.models import Category, Genre, Title


class LimitPutRequest(viewsets.ModelViewSet):

    http_method_names = ('get', 'post', 'patch', 'delete',)


class TitleViewSet(LimitPutRequest):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('id')
    serializer_class = TitleReadSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return TitleReadSerializer
        return TitlePostSerializer


class BaseListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


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
