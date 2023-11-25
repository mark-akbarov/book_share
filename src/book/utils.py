import random

import telebot

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


def save_user_phone_number(phone_number: str) -> User:
    """
    Saves the chat ID of a Telegram user to the database.

    Args:
        chat_id (str): The chat ID of the Telegram user.

    Returns:
        User: The User object associated with the given chat ID.

    Raises:
        ValueError: If the chat ID is not a valid string.
    """

    # if not isinstance(phone_number, str):
    #     raise ValueError("Chat ID must be a string")

    user, created = User.objects.create(phone_number=phone_number)
    if created:
        print(f"Created new user with chat ID: {phone_number}")

    return user


def request_book_from_code(code: int) -> Book:
    try: 
        return Book.objects.get(code=code)
    except Book.DoesNotExist:
        raise ValueError("Instance doesn't exist")


def add_book_to_db(book: Book) -> Book:
    code = generate_unique_code()
    
    
