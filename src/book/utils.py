import random

import telebot

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
    try: 
        return Book.objects.filter(Q(code=message) | Q(title__icontains=message))
    except Book.DoesNotExist:
        raise ValueError("Instance doesn't exist")


def get_telegram_username_by_chat_id(chat_id):
    return


def book_data_to_message(book_data: dict):
    title = book_data['title']
    author = book_data['author']
    genre = book_data['genre']
    condition  = book_data['condition']
    language = book_data['language']
    # photo = book_data['telegram_photo_id']
    book = f"""
Title: {title}
Author: {author}
Genre: {genre}
Condition: {condition}
Language: {language}
    """
    return book