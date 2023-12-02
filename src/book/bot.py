import enum
import json
from dataclasses import dataclass

from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import models

from telebot import TeleBot, types, custom_filters

from core.settings import REQUEST_BOT_TOKEN

from account.models.account import User
from book.models.book import Book, BookRequest, Request, Condition, Genre, Language, AvailabilityStatus
from book.models.borrow import BorrowedBook
from book.utils import (
    save_user_phone_number, 
    request_book_from_code,
    generate_unique_code,
    book_data_to_message
    )
from book.keyboard_markups import (
    KeyboardMarkup,
    yes_no_markup, 
    share_markup, 
    genre_markup, 
    condition_markup, 
    language_markup
    )


class BookOperationState(models.TextChoices):
    UPDATE = 'Update'
    CREATE = 'Create'


class UpdateBook(models.TextChoices):
    UPDATE_TITLE = 'title'
    UPDATE_AUTHOR = 'author'
    UPDATE_GENRE = 'genre'
    UPDATE_CONDITION = 'condition'
    UPDATE_PHOTO = 'telegram_photo_id'
    UPDATE_LANGUAGE = 'language'


class AddBookState(models.TextChoices):
    INPUT_TITLE = 'Title'
    INPUT_AUTHOR = 'Author'
    INPUT_GENRE = 'Genre'
    INPUT_CONDITION = 'Condition'
    INPUT_PHOTO = 'Photo'
    INPUT_LANGUAGE = 'Language'
    

class StartState(enum.Enum):
    SHARE_CONTACT = 'Share Contact'

    
class RequestBookState(enum.Enum):
    BOOK_CODE = 'Request Code'
    # BOOK_TITLE = 'request_title'
    # BOOK_AUTHOR = 'request_author'


def display_book_data(book):
    book_data = f"""
#{book.code}
Title: {book.title}
Author: {book.author}
Genre: {book.genre}
Condition: {book.condition}
Language: {book.language}
Status: {book.status}
Description: {book.description}
"""
    return book_data


def set_state(message, state):
    bot.set_state(message.from_user.id, state=state)
    

def get_state(message):
    return bot.get_state(message.from_user.id, message.chat.id)


book_info = {}
update_book = False
requested_user: User
requested_book_id: int


bot = TeleBot(REQUEST_BOT_TOKEN)
bot.add_custom_filter(custom_filters.StateFilter(bot))


@csrf_exempt
def webhook(request):
    data = json.loads(request.body)
    update = types.Update.de_json(data)
    bot.process_new_updates([update])
    return HttpResponse()


@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.reply_to(
        message, 
"""
This bot can help you to request your favorite books.
In addition, you can add your books to share with people.

List of commands:

/start - start working with the bot
/request - request a book by title or code
/add - add your books
/help - list of commands
/cancel - cancel the current operation
"""
        )


@bot.message_handler(commands=['cancel'])
def process_cancel(message):
    bot.delete_state(message.from_user.id, message.chat.id)
    bot.reply_to(
        message, 
        f"Command has been canceled. Send /help for a list of commands."
        )


@bot.message_handler(commands=['start'])
def handle_start_command(message):
    bot.send_message(
        message.chat.id, 
        'Please share your phone number to proceed.',
        reply_markup=share_markup.create(request_contact=True)
        )
    bot.set_state(message.from_user.id, state=StartState.SHARE_CONTACT.value)


@bot.message_handler( 
    content_types=['contact'],
    func=lambda message: get_state(message) == StartState.SHARE_CONTACT.value
    )
def handle_contact(message):
    phone_number = message.contact.phone_number
    bot.send_message(
        message.chat.id, 
        'Thank you for sharing your phone number!', 
        reply_markup=types.ReplyKeyboardRemove()
        )
    bot.delete_state(message.from_user.id, message.chat.id)
    save_user_phone_number(phone_number)


@bot.message_handler(commands=['mysharedbooks'])
def handle_my_books(message):
    books = Book.objects.filter(shared_by_telegram_user=message.chat.id)
    for book in books:
        bot.send_photo(
            message.chat.id,
            book.telegram_photo_id,
            display_book_data(book)
            )


@bot.message_handler(commands=['myborrows'])
def handle_my_borrows(message):
    books = BorrowedBook.objects.filter(book__shared_by_telegram_user=message.chat.id)
    if books:
        for book in books:
            bot.send_photo(
                message.chat.id,
                book.telegram_photo_id,
                display_book_data(book)
                )
    else:
        bot.reply_to(message, "You don't have borrowed books.")


@bot.message_handler(commands=['myrequests'])
def handle_my_request_books(message):
    book_requests = BookRequest.objects.filter(telegram_user_id=message.chat.id)
    if book_requests:
        for request in book_requests:
            bot.reply_to(
                message,
                display_book_data(request) + f"\nStatus: {request.status}"
                )
    else:
        bot.reply_to(message, "You don't have requested books.")


@bot.message_handler(state=StartState.SHARE_CONTACT.value)
def handle_contact_errors(message):
    if message.content_type != 'contact':  
        bot.reply_to(message, 'Please share phone number using button!')


@bot.message_handler(commands=['request'])
def handle_request_book(message):
    bot.reply_to(message, "Input Book's title or unique code")
    bot.set_state(message.from_user.id, RequestBookState.BOOK_CODE.value, message.chat.id)
    

@bot.message_handler(state=RequestBookState.BOOK_CODE.value)
def process_request_book(message):
    global requested_user
    requested_user = message.from_user.username
    title_or_code = message.text
    books = request_book_from_code(title_or_code)
    if len(books) > 0:        
        for book in books:
            book_data = display_book_data(book)
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Request Book", callback_data="Request Book"))
            bot.send_photo(message.chat.id, book.telegram_photo_id, book_data, reply_markup=markup)
        bot.set_state(message, handle_request_book)
    elif len(books) == 0:
        bot.send_message(message.chat.id, "Book not found")
        bot.set_state(message.from_user.id, RequestBookState.BOOK_CODE.value)


@bot.callback_query_handler(func=lambda call: call.data=="Request Book")
def handle_request_book(call):
    bot.answer_callback_query(call.id, "Your request has been sent. Waiting for approval...")
    print(requested_book_id)
    try:
        book = Book.objects.get(id=requested_book_id)
        print(book)
    except Book.DoesNotExist:
        bot.reply_to("Book does not exist")
    book_request = BookRequest.objects.create(
        telegram_user_id=requested_user, 
        book=book, 
        status=Request.WAITING_FOR_RESPONSE
        )
    print(book_request)
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        types.InlineKeyboardButton("Accept", callback_data='Accept'), 
        types.InlineKeyboardButton("Reject", callback_data='Reject')
        )
    bot.send_message(
        book.shared_by_telegram_user, 
        text=f"""
Book has been requested by @{requested_user}
#{book.code}
Title: {book.title}
Author: {book.author}
""", 
        reply_markup=markup
        )


@bot.callback_query_handler(func=lambda call: call.data == 'Accept')
def handle_accept_request_book(call):
    book_request = BookRequest(telegram_user_id=requested_user, book=requested_book_id)
    book_request.status = Request.ACCEPTED
    book_request.save()
    bot.answer_callback_query(call.id, "Thanks for sharing. :)")


@bot.callback_query_handler(func=lambda call: call.data == 'Reject')
def handle_accept_request_book(call):
    book_request = BookRequest(telegram_user_id=requested_user, book=requested_book_id)
    book_request.status = Request.REJECTED
    book_request.save()
    bot.answer_callback_query(call.id, "Book request has been rejected.")


@bot.message_handler(commands=['add'])
def handle_add_book(message):
    bot.reply_to(message, "Input title of your book")
    bot.set_state(message.from_user.id, state=AddBookState.INPUT_TITLE.value)
    

@bot.message_handler(state=AddBookState.INPUT_TITLE.value)
def handle_add_book_title(message):
    if len(message.text) <= 1:
        bot.reply_to(message, 'Please input a valid title')
        set_state(message, state=AddBookState.INPUT_TITLE.value)
        return
    book_info['Title'] = message.text
    if update_book:
        bot.reply_to(message, "Successfully changed", reply_markup=yes_no_markup.create())
        set_state(message, state='HANDLE CONFIRMATION')
        return
    set_state(message, state=AddBookState.INPUT_AUTHOR.value)
    bot.reply_to(message, "Input author of your book")


@bot.message_handler(state=AddBookState.INPUT_AUTHOR.value)
def handle_add_book_author(message):
    if len(message.text) <= 1:
        bot.reply_to(message, 'Type a valid author name.')
        bot.set_state(message.from_user.id, state=AddBookState.INPUT_AUTHOR.value)        
        return
    bot.delete_state(message.from_user.id, message.chat.id)
    book_info['Author'] = message.text
    if update_book:
        bot.reply_to(message, "Successfully changed", reply_markup=yes_no_markup.create())
        bot.set_state(message.from_user.id, state='HANDLE CONFIRMATION')
        return
    bot.reply_to(message, "Input genre of your book:", reply_markup=genre_markup.create())
    bot.set_state(message.from_user.id, state=AddBookState.INPUT_GENRE.value)


@bot.message_handler(state=AddBookState.INPUT_GENRE.value)
def handle_add_book_genre(message):
    if message.text not in Genre:
        bot.reply_to(message, 'Please choose genre from below')
        return
    bot.delete_state(message.from_user.id, message.chat.id)
    book_info['Genre'] = message.text
    if update_book:
        bot.reply_to(message, "Successfully changed", reply_markup=yes_no_markup.create())
        bot.set_state(message.from_user.id, state='HANDLE CONFIRMATION')
        return
    bot.set_state(message.from_user.id, state=AddBookState.INPUT_CONDITION.value)
    bot.send_message(
        chat_id=message.chat.id,  
        text="Choose condition of your book:", 
        reply_to_message_id=message.message_id,
        reply_markup=condition_markup.create_sliced(2)
        )


@bot.message_handler(state=AddBookState.INPUT_CONDITION.value)
def handle_add_book_condition(message):
    if message.text not in Condition:
        bot.reply_to(message, 'Please choose condition from below')
        return
    bot.delete_state(message.from_user.id, message.chat.id)
    book_info['Condition'] = message.text
    if update_book:
        bot.reply_to(message, "Successfully changed", reply_markup=yes_no_markup.create())
        bot.set_state(message.from_user.id, state='HANDLE CONFIRMATION')
        return
    bot.set_state(message.from_user.id, state=AddBookState.INPUT_LANGUAGE.value)        
    bot.send_message(
        chat_id=message.chat.id,  
        text="Choose language of your book:", 
        reply_to_message_id=message.message_id,
        reply_markup=language_markup.create()
        )


@bot.message_handler(state=AddBookState.INPUT_LANGUAGE.value)
def handle_add_book_language(message):
    if message.text not in Language:
        bot.reply_to(message, 'Please choose language from below')
        bot.set_state(message.from_user.id, state=AddBookState.INPUT_PHOTO.value)        
        return
    bot.delete_state(message.from_user.id, message.chat.id)
    book_info['Language'] = message.text
    if update_book:
        bot.reply_to(message, "Successfully changed", reply_markup=yes_no_markup.create())
        bot.set_state(message.from_user.id, state='HANDLE CONFIRMATION')
        return
    bot.set_state(message.from_user.id, state=AddBookState.INPUT_PHOTO.value)
    bot.send_message(
            chat_id=message.chat.id,
            text="Upload photo of the book:", 
            reply_to_message_id=message.message_id,
        )
    

@bot.message_handler(content_types=['photo'], state=AddBookState.INPUT_PHOTO.value)
def handle_add_book_photo(message):
    photo_id = message.photo[-1].file_id
    book_info['Photo'] = photo_id
    title = book_info['Title']
    author = book_info['Author']
    genre = book_info['Genre']
    condition  = book_info['Condition']
    language = book_info['Language']
    photo = book_info['Photo']
    book = f"""
Title: {title}
Author: {author}
Genre: {genre}
Condition: {condition}
Language: {language}
"""
    bot.delete_state(message.from_user.id, message.chat.id)
    bot.send_photo(message.chat.id, photo=photo, caption=book, reply_markup=yes_no_markup.create())
    bot.set_state(message.from_user.id, state='HANDLE CONFIRMATION')


@bot.message_handler(state=AddBookState.INPUT_PHOTO.value)
def handle_add_book_photo_errors(message):
    bot.reply_to(message, "Photo must in valid Image formats: jpg, jpeg, img")
    bot.set_state(message.from_user.id, AddBookState.INPUT_PHOTO.value, message.chat.id)


@bot.message_handler(state=['HANDLE CONFIRMATION'])
def handle_confirmation(message):
    global update_book
    if message.text == 'Yes, proceed':
        bot.send_message(message.chat.id, 'Your book details have been saved!')
        book = Book(
            title=book_info['Title'],
            author=book_info['Author'],
            genre=book_info['Genre'],
            condition=book_info['Condition'],
            language=book_info['Language'],
            shared_by_telegram_user=message.chat.id, 
            code=generate_unique_code(),
            status=AvailabilityStatus.AVAILABLE,
            telegram_photo_id=book_info['Photo'], 
            )
        book.save()
        post_body = book_data_to_message(book_info)
        bot.send_photo(message.chat.id, book.telegram_photo_id, post_body)
        update_book = False
        
    elif message.text == 'No, change details':
        update_book = True
        markup = KeyboardMarkup(AddBookState)
        bot.send_message(
            message.chat.id, 
            'Which part do you want to change?', 
            reply_markup=markup.create_sliced(2),
            reply_to_message_id=message.message_id
            )
        bot.set_state(message.from_user.id, 'HANDLE UPDATE INFO', message.chat.id)


@bot.message_handler(state='HANDLE UPDATE INFO')
def handle_update_info(message):
    state_to_choices_map = {
        AddBookState.INPUT_GENRE.value: Genre, 
        AddBookState.INPUT_CONDITION.value: Condition,
        AddBookState.INPUT_LANGUAGE: Language
        }
    if message.text in (
        AddBookState.INPUT_GENRE.value, 
        AddBookState.INPUT_CONDITION.value, 
        AddBookState.INPUT_LANGUAGE
        ):
        markup = KeyboardMarkup(state_to_choices_map.get(message.text))
        bot.send_message(
            message.chat.id, 
            f"Changing {message.text}:", 
            reply_to_message_id=message.message_id,
            reply_markup=markup.create(),
            )
    elif message.text in (
        AddBookState.INPUT_TITLE, 
        AddBookState.INPUT_AUTHOR, 
        AddBookState.INPUT_PHOTO
        ):
        bot.reply_to(
            message, 
            f"Changing {message.text}:", 
        )
    bot.set_state(message.from_user.id, message.text, message.chat.id)
