from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    filters,
    generics,
    mixins,
    pagination,
    permissions,
    status,
    viewsets,
)
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Review, Title
from users.models import CustomUser

from .filters import TitleFilter
from .pagination import PageNumberPagination
from .permissions import AdminOrReadOnly, Admin, UserAdminModeratorOrReadOnly
from .serializers import (
    AboutSerializer,
    CategorySerializer,
    CommentSerializer,
    CreateUserSerializer,
    GenreSerializer,
    MyTokenSerializer,
    ReviewSerializer,
    TitlePostSerializer,
    TitleReadSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (Admin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    lookup_field = "username"
    lookup_url_kwarg = "username"
    pagination_class = pagination.LimitOffsetPagination
    http_method_names = ("get", "post", "patch", "delete")

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
            user, _ = CustomUser.objects.get_or_create(
                email=email, username=username
            )
        except IntegrityError:
            return Response(
                "Такая почта или имя пользователя существует",
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
    if default_token_generator.check_token(user, confirmation_code):
        token = str(AccessToken.for_user(user))
        return Response(
            {"acces_token": token},
            status=status.HTTP_200_OK,
        )
    return Response("Не верный токен", status=status.HTTP_400_BAD_REQUEST)


class LimitPutRequest(viewsets.ModelViewSet):
    http_method_names = (
        "get",
        "post",
        "patch",
        "delete",
    )


class TitleViewSet(LimitPutRequest):
    queryset = Title.objects.annotate(
        rating=Avg("reviews__score")).order_by("id")
    serializer_class = TitleReadSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return TitleReadSerializer
        return TitlePostSerializer


class BaseListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class GenreViewSet(BaseListCreateDestroyViewSet):
    """
    Получить список всех жанров. Права доступа: Доступно без токена
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(BaseListCreateDestroyViewSet):
    """
    Получить список всех категорий. Права доступа: Доступно без токена
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Для модели отзыва."""

    serializer_class = ReviewSerializer
    permission_classes = (UserAdminModeratorOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get("title_id"))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title_id=self.get_title().id)


class CommentViewSet(viewsets.ModelViewSet):
    """Для модели комментариев."""

    serializer_class = CommentSerializer
    permission_classes = (UserAdminModeratorOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_review(self):
        return get_object_or_404(
            Review,
            id=self.kwargs.get("review_id"),
            title_id=self.kwargs.get("title_id"),
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, review_id=self.get_review().id)
