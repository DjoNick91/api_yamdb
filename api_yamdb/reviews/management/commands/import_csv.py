from django.core.management import BaseCommand
from django.db import transaction
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import CustomUser
import csv


class Command(BaseCommand):
    help = "Импорт данных из csv файлов в базу данных"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        # Импорт данных из category.csv
        with open("static/data/category.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            Category.objects.all().delete()
            Category.objects.bulk_create(
                [Category(name=row["name"]) for row in reader]
            )

        # Импорт данных из comments.csv
        with open("static/data/comments.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            Comment.objects.all().delete()
            Comment.objects.bulk_create(
                [Comment(text=row["text"]) for row in reader]
            )

        # Импорт данных из genre.csv
        with open("static/data/genre.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            Genre.objects.all().delete()
            Genre.objects.bulk_create(
                [Genre(name=row["name"]) for row in reader]
            )

        # Импорт данных из review.csv
        with open("static/data/review.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            Review.objects.all().delete()
            Review.objects.bulk_create(
                [Review(text=row["text"]) for row in reader]
            )

        # Импорт данных из titles.csv
        with open("static/data/titles.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            Title.objects.all().delete()
            Title.objects.bulk_create(
                [Title(name=row["name"]) for row in reader]
            )

        # Импорт данных из users.csv
        with open("static/data/users.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            CustomUser.objects.all().delete()
            CustomUser.objects.bulk_create(
                [CustomUser(username=row["username"], email=row["email"])
                 for row in reader]
            )
