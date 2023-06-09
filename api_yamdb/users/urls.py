from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import UserViewSet, new_user

app_name = "users"

router = routers.DefaultRouter()
router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    path("auth/token/", TokenObtainPairView.as_view(), name="get_token"),
    path("auth/signup/", new_user),
    path("", include(router.urls)),
]
