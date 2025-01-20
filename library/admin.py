from django.contrib import admin
from django.utils.html import format_html
from .models import Genre, Author, Language, Book


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')
    search_fields = ('first_name', 'last_name')
    ordering = ('last_name', 'first_name')


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('book_name', 'author', 'publish_date', 'isbn', 'language',  'cover_preview',)
    list_filter = ('genre', 'author', 'language', 'publish_date')
    search_fields = ('book_name', 'author__first_name', 'author__last_name', 'isbn')
    filter_horizontal = ('genre',)
    ordering = ('publish_date', 'book_name')
    readonly_fields = ('cover_preview',)
    fieldsets = (
        (None, {
            'fields': ('book_name', 'author', 'description', 'isbn', 'language', 'publish_date', 'cover',)
        }),
        ('Genres', {
            'fields': ('genre',),
        })
    )

    def cover_preview(self, obj):
        if obj.cover:
             return format_html('<img src="{}" width="150"/>'.format(obj.cover.url))
        return 'No Cover'
    cover_preview.short_description = 'Book Cover Preview'
