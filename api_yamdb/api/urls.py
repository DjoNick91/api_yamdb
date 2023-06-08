from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (CategoryViewSet,
                    GenreViewSet,
                    TitleViewSet,
                    ReviewViewSet,
                    CommentViewSet)

router = SimpleRouter()
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"titles", TitleViewSet)
router.register(r"genres", GenreViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='Reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='Comments'
)

urlpatterns = [
    path("api/v1/", include(router.urls)),
]
