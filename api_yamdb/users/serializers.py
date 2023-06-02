from rest_framework import serializers

from .models import CustomUser, ROLE


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=ROLE)

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
