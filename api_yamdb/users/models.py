from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE = [
    ("user", "Пользователь"),
    ("moderator", "Модератор"),
    ("admin", "Администратор"),
]


class CustomUser(AbstractUser):
    email = models.EmailField(
        max_length=254,
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
