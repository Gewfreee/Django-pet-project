from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Book, Author, Genre, Language, User
from django.db.models import Q
from .forms import ReviewForm, AuthorForm
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from . import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.cache import cache


def main(request):
    return render(request, 'main.html')

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    bookmarks = user.bookmarks.all()

    return render(request, 'profile.html', {'user' : user, 'bookmarks' : bookmarks})

def book(request):
    query = request.GET.get('q')
    cache_key = f'{query}'
    books = cache.get(cache_key)
    print(f'cache - {books}')

    if books is None:
        if query and query != '':
            q_objects = (
                    Q(book_name__icontains=query) |
                    Q(genre__name__icontains=query) |
                    Q(isbn__icontains=query) |
                    Q(author__first_name__icontains=query) |
                    Q(author__last_name__icontains=query)
            )
            if ' ' in query:
                first_name, *last_name = query.split()
                if last_name:
                    last_name = ' '.join(last_name)
                    q_objects |= (
                            Q(author__first_name__icontains=first_name) & Q(author__last_name__icontains=last_name))
            books = Book.objects.filter(q_objects).distinct().order_by('book_name')
            print(f'books - {books}')
            cache.set(cache_key, list(books), timeout=1200)
        else:
            books = Book.objects.none()
            print(f'books - {books}')

    return render(request, 'main.html', {'page_obj': books})

def book_page(request, book_name):
    book = get_object_or_404(Book, book_name=book_name)
    reviews = book.reviews.all().order_by('created_at')
    user_review = None
    is_bookmarked = False

    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()

        if request.method == 'POST' and 'toggle_bookmark' in request.POST:
            is_bookmarked = book in request.user.bookmarks.all()
            if is_bookmarked:
                request.user.bookmarks.remove(book)
                is_bookmarked = False
            else:
                request.user.bookmarks.add(book)
                is_bookmarked = True
            return JsonResponse({'bookmarked': is_bookmarked})

    form = ReviewForm(instance=user_review) if user_review else ReviewForm()

    return render(request, 'book_page.html', {'book' : book, 'form' : form, 'reviews' : reviews,
                                              'is_bookmarked' : is_bookmarked, 'user_review' : user_review})

def author_page(request, pk):
    author = get_object_or_404(Author, pk=pk)
    form = AuthorForm(instance=author) if author else ReviewForm()

    return render(request, 'author_page.html', {'form' : form, 'author' : author})

@login_required
def add_review(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = book.reviews.all()
    user_review = reviews.filter(user=request.user).first()

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=user_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            return redirect('book_page', book_name=book.book_name)

    return render(request, 'book_page.html', {'book': book, 'reviews': reviews})


# API views
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def book_list(request):
    books = Book.objects.all()
    serializer = serializers.BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    serializer = serializers.BookSerializer(book)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def author_list(request):
    authors = Author.objects.all()
    serializer = serializers.AuthorSerializer(authors, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    serializer = serializers.AuthorSerializer(author)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def genre_list(request):
    genres = Genre.objects.all()
    serializer = serializers.GenreSerializer(genres, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def genre_detail(request, pk):
    genre = get_object_or_404(Genre, pk=pk)
    serializer = serializers.GenreSerializer(genre)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def language_list(request):
    languages = Language.objects.all()
    serializer = serializers.LanguageSerializer(languages, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def language_detail(request, pk):
    language = get_object_or_404(Language, pk=pk)
    serializer = serializers.LanguageSerializer(language)
    return Response(serializer.data)
