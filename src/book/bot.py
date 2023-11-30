import enum
import json

from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import models

from telebot import TeleBot, types, custom_filters

from core.utils.validations import validate_phone_number
from core.settings import REQUEST_BOT_TOKEN

from book.models.book import Book, Condition, Genre, Language, AvailabilityStatus
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


book_info = {}
update_book = False

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
        f"Command {message.text[1:]} has been canceled. Send /help for a list of commands."
        )


@bot.message_handler(commands=['start'])
def handle_start_command(message):
    bot.send_message(
        message.chat.id, 
        'Please share your phone number to proceed.',
        reply_markup=share_markup.create(request_contact=True)
        )
    bot.register_next_step_handler(message, handle_contact)


@bot.message_handler(commands=['request'])
def handle_request_book(message):
    bot.reply_to(message, "Input Book's title or unique code")
    bot.set_state(message.from_user.id, RequestBookState.BOOK_CODE.value, message.chat.id)
    bot.register_next_step_handler(message, process_request_book)


@bot.message_handler(commands=['add'])
def handle_add_book(message):
    bot.reply_to(message, "Input title of your book")
    bot.register_next_step_handler(message, handle_add_book_title)


@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    if message.content_type != 'contact':
        bot.reply_to(message, 'Please share phone number with keyboard!')
        bot.register_next_step_handler(message, handle_contact)
    phone_number = message.contact.phone_number
    bot.send_message(
        message.chat.id, 
        'Thank you for sharing your phone number!', 
        reply_markup=types.ReplyKeyboardRemove()
        )
    save_user_phone_number(phone_number)


@bot.message_handler(state=RequestBookState.BOOK_CODE.value)
def process_request_book(message):
    title_or_code = message.text
    books = request_book_from_code(title_or_code)
    if len(books) > 0:        
        for book in books:
            book_data = display_book_data(book)
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Request Book", callback_data=book.id))
            bot.send_photo(message.chat.id, book.telegram_photo_id, book_data, reply_markup=markup)
        bot.register_next_step_handler(message, handle_request_book)
    elif len(books) == 0:
        bot.send_message(message.chat.id, "Book not found")
        bot.register_next_step_handler(message, process_request_book)


@bot.callback_query_handler(func=lambda call: True)
def handle_request_book(call):
    book_id = call.data
    book = Book.objects.get(id=book_id)
    bot.answer_callback_query(call.id, "Your request has been sent. Waiting for approval...")
    bot.send_message(book.shared_by_telegram_user, "Request has been made for one of your books")


@bot.message_handler(state=AddBookState.INPUT_TITLE.value)
def handle_add_book_title(message):
    if len(message.text) <= 1:
        bot.reply_to(message, 'Book title cannot be empty')
        bot.register_next_step_handler(message, handle_add_book_title)
        return
    book_info['Title'] = message.text
    if update_book:
        bot.reply_to(message, "Successfully changed", reply_markup=yes_no_markup.create())
        bot.register_next_step_handler(message, handle_confirmation)
        return
    bot.reply_to(message, "Input author of your book")
    bot.register_next_step_handler(message, handle_add_book_author)


@bot.message_handler(state=AddBookState.INPUT_AUTHOR.value)
def handle_add_book_author(message):
    if len(message.text) <= 1:
        bot.reply_to(message, 'Type a valid author name.')
        bot.register_next_step_handler(message, handle_add_book_author)
        return
    if update_book:
        bot.reply_to(message, "Successfully changed", reply_markup=yes_no_markup.create())
        bot.register_next_step_handler(message, handle_confirmation)
        return
    bot.reply_to(message, "Input genre of your book:", reply_markup=genre_markup.create())
    bot.register_next_step_handler(message, handle_add_book_genre)
    book_info['Author'] = message.text


@bot.message_handler(state=AddBookState.INPUT_GENRE.value)
def handle_add_book_genre(message):
    if message.text not in Genre:
        bot.reply_to(message, 'Please choose genre from below')
        bot.register_next_step_handler(message, handle_add_book_genre)
        return
    
    book_info['Genre'] = message.text
    if update_book:
        bot.reply_to(message, "Successfully changed", reply_markup=yes_no_markup.create())
        bot.register_next_step_handler(message, handle_confirmation)
        return
    bot.send_message(
        chat_id=message.chat.id,  
        text="Choose condition of your book:", 
        reply_to_message_id=message.message_id,
        reply_markup=condition_markup.create_sliced(2)
        )
    bot.register_next_step_handler(message, handle_add_book_condition)


@bot.message_handler(state=AddBookState.INPUT_CONDITION.value)
def handle_add_book_condition(message):
    if message.text in Condition:
        if update_book:
            bot.reply_to(message, "Successfully changed", reply_markup=yes_no_markup.create())
            bot.register_next_step_handler(message, handle_confirmation)
            return  
        bot.send_message(
            chat_id=message.chat.id,  
            text="Choose language of your book:", 
            reply_to_message_id=message.message_id,
            reply_markup=language_markup.create()
            )
        book_info['Condition'] = message.text
        bot.register_next_step_handler(message, handle_add_book_language)        
    else:
        bot.reply_to(message, 'Please choose condition from below')
        bot.register_next_step_handler(message, handle_add_book_condition)       


@bot.message_handler(state=AddBookState.INPUT_LANGUAGE.value)
def handle_add_book_language(message):
    if message.text not in Language:
        bot.reply_to(message, 'Please choose language from below')
        bot.register_next_step_handler(message, handle_add_book_language)
        return
    book_info['Language'] = message.text
    if update_book:
        bot.reply_to(message, "Successfully changed", reply_markup=yes_no_markup.create())
        bot.register_next_step_handler(message, handle_confirmation)
        return
    bot.send_message(
            chat_id=message.chat.id,
            text="Upload photo of the book:", 
            reply_to_message_id=message.message_id,
        )
    bot.register_next_step_handler(message, handle_add_book_photo)


@bot.message_handler(content_types=['photo'], state=AddBookState.INPUT_PHOTO.value)
def handle_add_book_photo(message):
    if message.content_type != 'photo':
        bot.reply_to(message, "Please send a photo file of the book's cover.")
        bot.register_next_step_handler(message, handle_add_book_photo)
        return
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
    bot.send_photo(message.chat.id, photo=photo, caption=book, reply_markup=yes_no_markup.create())
    bot.register_next_step_handler(message, process_handle_info)


def process_handle_info(message):
    if message.text == 'Yes, proceed':
        bot.send_message(message.chat.id, 'Your book details have been saved!')
        print(book_info)
        
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
    elif message.text == 'No, change details':
        global update_book
        update_book = True
        markup = KeyboardMarkup(AddBookState)
        bot.send_message(
            message.chat.id, 
            'Which part do you want to change?', 
            reply_markup=markup.create_sliced(2),
            reply_to_message_id=message.message_id
            )
        bot.register_next_step_handler(message, handle_confirmation)


def handle_confirmation(message):
    enum_dict = {Genre.__name__: Genre, Condition.__name__: Condition, Language.__name__: Language}
    if message.text in enum_dict:
        markup = KeyboardMarkup(enum_dict.get(message.text))
        func = func_list[message.text]
        bot.send_message(
            message.chat.id, 
            f"Changing {message.text}:", 
            reply_to_message_id=message.message_id,
            reply_markup=markup.create(),
            )
        bot.register_next_step_handler(message, func)
    elif message.text in ['Title', 'Author']:
        bot.send_message(
            message.chat.id, 
            f"Changing {message.text}:", 
            reply_to_message_id=message.message_id,
            )
        func = func_list[message.text]
        bot.register_next_step_handler(message, func)
    elif message.text == 'Photo':
        bot.send_message(
            message.chat.id, 
            f"Upload {message.text}:", 
            reply_to_message_id=message.message_id,
            )
        func = func_list[message.text]
        bot.register_next_step_handler(message, handle_add_book_photo)


func_list = {
    'Title': handle_add_book_title, 
    'Author': handle_add_book_author, 
    'Genre': handle_add_book_genre, 
    'Condition': handle_add_book_condition,
    'Language': handle_add_book_language,
    'Photo': handle_add_book_photo,
    }