from django.core.management import BaseCommand
from django.db import transaction
import pandas as pd
from reviews.models import Category, Comment, Genre, Review, Title, User


class Command(BaseCommand):
    help = "Импорт данных из csv файлов в базу данных"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        # Чтение данных из category.csv и их импорт в базу данных
        df = pd.read_csv("static/data/category.csv")
        Category.objects.all().delete()  # Очистка таблицы перед импортом
        Category.objects.bulk_create(
            [Category(name=row["name"]) for _, row in df.iterrows()]
        )

        # Чтение данных из comments.csv и их импорт в базу данных
        df = pd.read_csv("static/data/comments.csv")
        Comment.objects.all().delete()
        Comment.objects.bulk_create(
            [Comment(text=row["text"]) for _, row in df.iterrows()]
        )

        # Чтение данных из genre.csv и их импорт в базу данных
        df = pd.read_csv("static/data/genre.csv")
        Genre.objects.all().delete()
        Genre.objects.bulk_create(
            [Genre(name=row["name"]) for _, row in df.iterrows()]
        )

        # Чтение данных из review.csv и их импорт в базу данных
        df = pd.read_csv("static/data/review.csv")
        Review.objects.all().delete()
        Review.objects.bulk_create(
            [Review(text=row["text"]) for _, row in df.iterrows()]
        )

        # Чтение данных из titles.csv и их импорт в базу данных
        df = pd.read_csv("static/data/titles.csv")
        Title.objects.all().delete()
        Title.objects.bulk_create(
            [Title(name=row["name"]) for _, row in df.iterrows()]
        )

        # Чтение данных из users.csv и их импорт в базу данных
        df = pd.read_csv("static/data/users.csv")
        User.objects.all().delete()
        User.objects.bulk_create(
            [User(username=row["username"], email=row["email"])
             for _, row in df.iterrows()]
        )
