from django.urls import include, path
from rest_framework import routers

from .views import CreateUserView, UserViewSet, crate_token

app_name = "api"

router = routers.DefaultRouter()
router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    path("auth/signup/", CreateUserView.as_view()),
    path("auth/token/", crate_token, name="get_token"),
    path("", include(router.urls)),
]
