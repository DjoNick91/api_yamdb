from rest_framework import mixins, viewsets, filters
from .permissions import (IsAdminOrReadOnly)


class BaseListCreateDestroyMixin(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class LimitPutRequestMixin(mixins.RetrieveModelMixin,
                           mixins.DestroyModelMixin):
    http_method_names = [
        "get",
        "post",
        "patch",
        "delete"
    ]
