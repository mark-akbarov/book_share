import random

from django.db.models import Q

from book.models import Book
from account.models.account import User


def generate_unique_code() -> int:
    """
    Generates a unique 4-digit code for a book.

    Returns:
        int: A unique 4-digit code for a book.
    """
    while True:
        code = random.randint(1000, 9999)
        if Book.objects.filter(code=code).exists():
            continue
        else:
            return code


def save_or_get_user(
    telegram_username: str, 
    telegram_user_id: int, 
    phone_number: str
    ) -> User:
    user, created = User.objects.get_or_create(
        phone_number=phone_number,
        telegram_username=telegram_username,
        telegram_user_id=telegram_user_id    
    )
    return created


def request_book_from_code(message: int) -> Book:
    books = Book.objects.filter(
        ~Q(shared_by=message.from_user.id), 
        Q(code=message.text) | Q(title__icontains=message.text)
        )
    
    return books


def book_data_to_message(book_data: dict):
    title = book_data['title']
    author = book_data['author']
    genre = book_data['genre']
    condition  = book_data['condition']
    language = book_data['language']
    book = f"""
Title: {title}
Author: {author}
Genre: {genre}
Condition: {condition}
Language: {language}
    """
    return book


def get_most_read_genre(books):
    genres = {}
    for book in books:
        if book.genre in genres:
               genres[book.genre] += 1
        else:
            genres[book.genre] = 1
    genre = max(genres, key=genres.get) 
    return genre


def recommend_books(genre):
    pass