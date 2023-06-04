import secrets
import string
from django.core.mail import send_mail

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer

from .models import ROLE, CustomUser, UserConfirm


class UserSerializer(serializers.ModelSerializer):
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


def generate_code():
    confirmation_code = "".join(
        secrets.choice(string.digits + string.ascii_letters) for i in range(30)
    )
    return confirmation_code


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("email", "username")
        model = CustomUser

    def create(self, validated_data):
        email = validated_data["email"]
        conf_code = generate_code()
        user = CustomUser.objects.get_or_create(**validated_data)
        UserConfirm.objects.get_or_create(user=user, confirmation_code=conf_code)
        send_mail(
            subject="Register on site YaMDb",
            message=("Код регистрации: " + conf_code),
            from_email=None,
            recipient_list=[email],
        )
        return user


class MyTokenSerializer(TokenObtainSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["confirmation_code"] = serializers.CharField()
