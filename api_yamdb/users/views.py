import secrets
import string
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import CustomUser
from .serializers import UserSerializer


def generate_code():
    confirmation_code = "".join(
        secrets.choice(string.digits + string.ascii_letters) for i in range(30)
    )
    return confirmation_code


def new_user(email, confirmation_code):
    send_mail(
        "Регистрация на сайте YaMDb",
        (
            f'{"Для регистрации на сайте YaMDb отправьте Ваш userneme и"}',
            f'{"полученный код подтверждений {confirmation_code}"}',
            f'{"на /api/v1/auth/token/"}',
        ),
        from_email=None,
        recipient_list=[email],
    )


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)

    @action(
        detail=False,
        methods=["get", "patch"],
        permission_classes=[permissions.IsAuthenticated],
        url_path="me",
    )
    def me_about(self, request):
        user = get_object_or_404(CustomUser, username=request.user.username)
        if request.method == "PATCH":
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK,
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
