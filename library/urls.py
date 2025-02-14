from django.urls import path
from library import views


urlpatterns = [
    path('', views.main, name='main'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('books/', views.book, name='book'),
    path('books/<str:book_name>/', views.book_page, name='book_page'),
    path('books/<int:pk>/add_review/', views.add_review, name='add_review'),
    path('books/<int:pk>', views.author_page, name='author_page'),

    # API routes
    path('api/books/', views.book_list, name='book_list'),
    path('api/books/<int:pk>/', views.book_detail, name='book_detail'),
    path('api/authors/', views.author_list, name='author_list'),
    path('api/authors/<int:pk>/', views.author_detail, name='author_detail'),
    path('api/genres/', views.genre_list, name='genre_list'),
    path('api/genres/<int:pk>/', views.genre_detail, name='genre_detail'),
    path('api/languages/', views.language_list, name='language_list'),
    path('api/languages/<int:pk>/', views.language_detail, name='language_detail'),
]

