import re

from rest_framework import serializers

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
