import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import ROLE, CustomUser


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=ROLE, default="user")

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
        if value == "me":
            raise serializers.ValidationError("Такое имя запрещено")
        return value


class AboutSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=ROLE, read_only=True)

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
        if value == "me":
            raise serializers.ValidationError("Такое имя запрещено")
        return value


class CreateUserSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True, max_length=254)

    def validate_username(self, value):
        username = value
        email = self.initial_data.get("email")
        if username == "me":
            raise serializers.ValidationError("Такое имя запрещено")
        if not re.match(r"^[\w.@+-]+$", username):
            raise serializers.ValidationError("Не корректный формал логина")
        if CustomUser.objects.filter(
            username=username
        ) and not CustomUser.objects.filter(email=email):
            raise serializers.ValidationError(
                "Не верная почта для этого пользователя",
            )
        if CustomUser.objects.filter(
            email=email
        ) and not CustomUser.objects.filter(username=username):
            raise serializers.ValidationError(
                "Пользователь с такой почтой уже существует"
            )
        return value


class MyTokenSerializer(serializers.Serializer):
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


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""
    author = SlugRelatedField(
        slug_field="username",
        read_only=True,
    )

    class Meta:
        fields = (
            "id",
            "text",
            "author",
            "score",
            "pub_date",
        )
        model = Review

    def validate(self, data):
        title_id = (
            self.context["request"].parser_context["kwargs"]["title_id"]
        )
        user = self.context["request"].user
        if (
            self.context["request"].method == "POST"
            and Review.objects.filter(author=user, title=title_id).exists()
        ):
            raise ValidationError(
                "Вы уже оставляли отзыв на это произведение."
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев"""
    author = SlugRelatedField(
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
