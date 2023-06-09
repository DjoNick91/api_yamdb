from django.urls import include, path
from rest_framework import routers

from .views import (CreateUserView, UserViewSet, crate_token, CategoryViewSet,
                    GenreViewSet, TitleViewSet, ReviewViewSet, CommentViewSet)

app_name = "api"

router = routers.DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"titles", TitleViewSet)
router.register(r"genres", GenreViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='Reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='Comments')

urlpatterns = [
    path("auth/signup/", CreateUserView.as_view()),
    path("auth/token/", crate_token, name="get_token"),
    path("", include(router.urls)),
]
