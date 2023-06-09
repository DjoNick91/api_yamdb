from django.contrib import admin

from .models import Category, Genre, Title


class TitleAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "display_genre", "description")
    search_fields = ("description", "name")
    list_filter = ("category", "year")
    empty_value_display = "-пусто-"

    def display_genre(self, obj):
        return ", ".join(genre.name for genre in obj.genre.all())

    display_genre.short_description = "Жанр"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    list_filter = ("name",)
    empty_value_display = "пусто"


class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    list_filter = ("name",)
    empty_value_display = "пусто"


admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
