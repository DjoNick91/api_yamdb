from django.contrib.auth.models import AbstractUser
from django.db import models


ROLE = ["user", "moderator", "admin"]


class CustomUser(AbstractUser):
    email = models.EmailField(
        max_length=254,
        required=True,
        unique=True,
    )

    bio = models.CharField(
        max_length=50,
        blank=True,
    )
    role = models.CharField(
        max_length=50,
        choices=ROLE,
        default="user",
    )

    def __str__(self):
        return self.username
