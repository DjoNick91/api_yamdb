from django.contrib.auth import views
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

app_name = "users"

urlpatterns = [
    path("auth/token/", TokenObtainPairView.as_view(), name="get_token"),
    path("auth/signup/", views.PasswordResetView.as_view()),
]
