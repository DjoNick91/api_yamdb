from django.db import models
from django.db.models import CustomUser
from django.core.validators import MaxValueValidator, MinValueValidator


class Category(models.Model):
    name = models.CharField(
        'Название',
        max_length=256,
    )
    slug = models.SlugField(
        'Слаг',
        max_length=50,
        unique=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        'Название',
        max_length=256,
    )
    slug = models.SlugField(
        'Слаг',
        max_length=50,
        unique=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.slug


class Title(models.Model):
    category = models.ForeignKey(
        Category,
        verbose_name='Slug категории',
    )
    genre = models.ManyToManyField(
        Genre,
        through='TitleGenre'
    )
    name = models.CharField(
        'Название',
        max_length=256,
    )
    year = models.IntegerField('Год выпуска')

    description = models.TextField(
        'Описание',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ('year', 'name')
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        default_related_name = 'titles'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre_id = models.ForeignKey(Genre)
    title_id = models.ForeignKey(Title)

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        related_name='reviews',
        verbose_name='Название',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        CustomUser,
        related_name='reviews',
        verbose_name='Автор',
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )
    text = models.TextField(
        null=False,
        blank=False,
        verbose_name='Текст',
    )
    score = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10,)
        ],
        verbose_name='Оценка'
    )

    class Meta:
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            ),
        ]


class Comment(models.Model):

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='review_id',
    )

    text = models.TextField(
        null=False,
        blank=False,
        verbose_name='comment_text',
    )

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='author_comment',
    )

    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        ordering = ["pub_date"]
