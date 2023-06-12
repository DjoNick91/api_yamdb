import re

from django.utils import timezone
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=CustomUser.USER_ROLE_CHOICES,
                                   default="user")

    class Meta:
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        model = CustomUser

    def validate_username(self, value):
        if value.casefold() == "me":
            raise serializers.ValidationError("Такое имя запрещено")
        return value


class AboutSerializer(UserSerializer):
    role = serializers.ChoiceField(choices=CustomUser.USER_ROLE_CHOICES,
                                   read_only=True)


class CreateUserSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True, max_length=254)

    def validate_username(self, value):
        username = value
        email = self.initial_data.get("email")
        user = CustomUser.objects.filter(username=username).exists()
        user_email = CustomUser.objects.filter(email=email).exists()
        if username.casefold() == "me":
            raise serializers.ValidationError("Такое имя запрещено")
        if not re.match(r"^[\w.@+-]+$", username):
            raise serializers.ValidationError("Не корректный формал логина")
        if user and not user_email:
            raise serializers.ValidationError(
                "Не верная почта для этого пользователя",
            )
        if user_email and not user:
            raise serializers.ValidationError(
                "Пользователь с такой почтой уже существует"
            )
        if user and user_email:
            if CustomUser.objects.filter(username=username,
                                         email=email).exists():
                return value
            raise serializers.ValidationError(
                "Такая почта или имя пользователя существует"
            )
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        fields = ("username", "confirmation_code")
        model = CustomUser


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ("id",)
        model = Category
        lookup_field = "slug"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ("id",)
        lookup_field = "slug"


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = "__all__"
        model = Title


class TitlePostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field="slug", queryset=Genre.objects.all(), many=True
    )
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = "__all__"

    def validate_year(self, value):
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError(
                "Год не может быть больше текущего года.")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
    )

    class Meta:
        model = Review
        fields = (
            "id",
            "text",
            "author",
            "score",
            "pub_date",
        )

    def validate(self, data):
        title_id = self.context["request"].parser_context["kwargs"]["title_id"]
        user = self.context["request"].user
        if (
            self.context["request"].method == "POST"
            and Review.objects.filter(author=user, title=title_id).exists()
        ):
            raise serializers.ValidationError(
                "Вы уже оставляли отзыв на это произведение."
            )
        return data

    def validate_score(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError("Оценка должна быть от 1 до 10.")
        return value


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев"""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )
        model = Comment
