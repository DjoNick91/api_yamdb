from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import CustomUser
from .validators import validate_year


class Category(models.Model):
    name = models.CharField(
        "Название",
        max_length=256,
    )
    slug = models.SlugField("Слаг", max_length=50, unique=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def str(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        "Название",
        max_length=256,
    )
    slug = models.SlugField("Слаг", max_length=50, unique=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def str(self):
        return self.slug


class Title(models.Model):
    category = models.ForeignKey(
        Category,
        verbose_name="Slug категории",
        on_delete=models.CASCADE,
    )
    genre = models.ManyToManyField(
        Genre,
    )
    name = models.CharField(
        "Название",
        max_length=256,
    )
    year = models.IntegerField(
        "Год выпуска",
        validators=[validate_year]
    )
    description = models.TextField("Описание", blank=True, null=True)

    class Meta:
        ordering = ("year", "name")
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
        default_related_name = "titles"

    def str(self):
        return self.name


class Review(models.Model):
    """Модель для работы с отзывами"""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='title',
    )
    text = models.TextField(
        null=False,
        blank=False,
        verbose_name='text_review',
    )
    # автор отзыва
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='author_review'
    )
    # рейтинг произведения, автора отзыва
    score = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1, "Минимально допустимая оценка: 1"),
            MaxValueValidator(10, "Максимально допустимая оценка: 10")
        ],
        verbose_name='score_review'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        # проверка один пользователь - один комментарий
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            ),
        ]
        # сортировка отзывов
        ordering = ["pub_date"]


class Comment(models.Model):
    """Модель для работы с комментариями к отзывам"""
    # id отзыва
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='review_id',
    )
    # текст комментария
    text = models.TextField(
        null=False,
        blank=False,
        verbose_name='comment_text',
    )
    # автор комментария
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='author_comment',
    )
    # дата публикации
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    # сортировка комментариев
    class Meta:
        ordering = ["pub_date"]
