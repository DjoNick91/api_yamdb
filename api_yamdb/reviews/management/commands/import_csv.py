from django.core.management import BaseCommand
from django.db import connections
import pandas as pd


class Command(BaseCommand):
    help = "Импорт данных из csv файлов в базу данных"

    def handle(self, *args, **kwargs):
        conn = connections["default"]

        # Чтение данных из category.csv и их импорт в базу данных
        df = pd.read_csv("static/data/category.csv")
        with conn.cursor() as cursor:
            cursor.copy_from(df, "reviews_category", sep=",", null="")
            conn.commit()

        # Чтение данных из comments.csv и их импорт в базу данных
        df = pd.read_csv("static/data/comments.csv")
        with conn.cursor() as cursor:
            cursor.copy_from(df, "reviews_comments", sep=",", null="")
            conn.commit()

        # Чтение данных из genre.csv и их импорт в базу данных
        df = pd.read_csv("static/data/genre.csv")
        with conn.cursor() as cursor:
            cursor.copy_from(df, "reviews_genre", sep=",", null="")
            conn.commit()

        # Чтение данных из review.csv и их импорт в базу данных
        df = pd.read_csv("static/data/review.csv")
        with conn.cursor() as cursor:
            cursor.copy_from(df, "reviews_review", sep=",", null="")
            conn.commit()

        # Чтение данных из titles.csv и их импорт в базу данных
        df = pd.read_csv("static/data/titles.csv")
        with conn.cursor() as cursor:
            cursor.copy_from(df, "reviews_title", sep=",", null="")
            conn.commit()

        # Чтение данных из users.csv и их импорт в базу данных
        df = pd.read_csv("static/data/users.csv")
        with conn.cursor() as cursor:
            cursor.copy_from(df, "users_user", sep=",", null="")
            conn.commit()
