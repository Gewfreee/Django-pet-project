from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='Book genre')

    def __str__(self):
            return self.name

    def get_absolute_url(self):
        return reverse('genre-detail', args=[str(self.id)])


class Author(models.Model):
    first_name = models.CharField(max_length=100, help_text='Author\'s name')
    last_name = models.CharField(max_length=100, help_text='Author\'s surname')
    bio = models.TextField(blank=True, help_text='Author\'s biography')

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])


class Language(models.Model):
    name = models.CharField(max_length=200, help_text='Language')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('language-detail', args=[str(self.id)])


class Book(models.Model):
    publish_date = models.DateField(blank=True, null=True)
    book_name = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    description = models.TextField(help_text='Book description')
    isbn = models.CharField('ISBN', max_length=13, help_text='ISBN')
    genre = models.ManyToManyField('Genre', help_text='Book genre')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    cover = models.ImageField(upload_to='book_covers/', null=True, blank=True)

    class Meta:
        ordering = ['publish_date', 'book_name']

    def __str__(self):
        return self.book_name

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

class User(AbstractUser):
    bookmarks = models.ManyToManyField('Book', blank=True, related_name='bookmarked_by')
    bio = models.TextField(blank=True)


class Review(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Review by {self.user.username} on {self.book.book_name}"
