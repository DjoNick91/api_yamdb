from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets, generics
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.tokens import default_token_generator


from users.models import CustomUser
from .serializers import (
    CreateUserSerializer,
    UserSerializer,
    MyTokenSerializer,
    AboutSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    lookup_field = "username"
    lookup_url_kwarg = "username"

    @action(
        detail=False,
        methods=["get", "patch"],
        permission_classes=[permissions.IsAuthenticated],
        url_path="me",
    )
    def me_about(self, request):
        user = get_object_or_404(CustomUser, username=request.user.username)
        if request.method == "PATCH":
            serializer = AboutSerializer(user, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
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


class CreateUserView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        username = serializer.validated_data.get("username")
        try:
            user, _ = CustomUser.objects.get_or_create(email=email, username=username)
        except IntegrityError:
            return Response(
                "Такая почта или имя польхователя существует",
                status=status.HTTP_400_BAD_REQUEST,
            )
        confirantion_code = default_token_generator.make_token(user)
        send_mail(
            subject="Register on site YaMDb",
            message=("Код регистрации: " + confirantion_code),
            from_email=None,
            recipient_list=[email],
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def crate_token(request):
    serializer = MyTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    confirmation_code = serializer.validated_data.get("confirmation_code")
    user = get_object_or_404(
        CustomUser, username=serializer.validated_data.get("username")
    )
    default_token_generator.check_token(user, confirmation_code)
    token = str(AccessToken.for_user(user))
    return Response(
        {"acces_token": token},
        status=status.HTTP_200_OK,
    )
