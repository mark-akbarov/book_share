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
    return Book.objects.get(code=code)


def add_book(book: Book) -> Book:
    if not isinstance(book, Book):
        raise ValueError("Must be a Book object")
    
    
    
# def submit_trailer_issue(driver: User, issue: str, photos: list, status: str):
#     # trailer_issue = TrailerIssue.objects.create(driver=driver, issue=issue, status=status)
#     # trailer_issue.photos.set(photos)
#     text = f"""
# Trailer Issue ID: {trailer_issue.id}
# Driver: {driver}
# Driver Type: {driver.driver_type}
# Issue Type: {issue}
# Status: {trailer_issue.status}
# Unit ID: {driver.unit_id}
# VIN ID: {driver.vin_id}
# Created Time: {trailer_issue.created_at.strftime("%B %d, %Y %I:%M %p")}
# Updated Time: {trailer_issue.updated_at.strftime("%B %d, %Y %I:%M %p")}
#     """
#     bot.send_media_group(chat_id=chat_id, media=send_compressed_photos(trailer_issue.photos.all(), caption=text))


# def send_compressed_photos(photos: list, caption: str):
#     photo_paths = [f"../media/{photo.image}" for photo in photos]
#     return [telebot.types.InputMediaPhoto(open(f"{photo_paths[num]}", "rb"), caption=caption if num == 0 else '') for num in range(len(photo_paths))]