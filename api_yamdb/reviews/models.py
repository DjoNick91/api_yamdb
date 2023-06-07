from django.db import models


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
        through="GenreTitle",
    )
    name = models.CharField(
        "Название",
        max_length=256,
    )
    year = models.IntegerField("Год выпуска")

    description = models.TextField("Описание", blank=True, null=True)

    class Meta:
        ordering = ("year", "name")
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
        default_related_name = "titles"

    def str(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def str(self):
        return f"{self.genre} {self.title}"
