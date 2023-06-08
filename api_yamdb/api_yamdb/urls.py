from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib import admin

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("api.urls", namespace="api")),
    path("redoc/", TemplateView.as_view(template_name="redoc.html"), name="redoc"),
]
