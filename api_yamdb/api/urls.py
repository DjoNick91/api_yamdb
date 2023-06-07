from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import CategoryViewSet, GenreViewSet, TitleViewSet

router = SimpleRouter()
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"titles", TitleViewSet)
router.register(r"genres", GenreViewSet)

urlpatterns = [
    path("api/v1/", include(router.urls)),
]
