from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ADMINISTRATOR = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    USER_ROLE_CHOICES = [
        (ADMINISTRATOR, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
    ]

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
        choices=USER_ROLE_CHOICES,
        default=USER,
    )

    def __str__(self):
        return self.username
