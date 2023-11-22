import enum
import json

from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from telebot import TeleBot, types, custom_filters

from core.utils.validations import validate_phone_number
from core.settings import REQUEST_BOT_TOKEN, GROUP_CHAT_ID

from book.models.book import Book
from book.serializers.book import BookCreateSerializer
from book.utils import save_user_phone_number, request_book_from_code, add_book


book_info = {}


class StartState(enum.Enum):
    SHARE_CONTACT = 'share_contact'

    
class RequestBookState(enum.Enum):
    BOOK_CODE = 'request_code'
    # BOOK_TITLE = 'request_title'
    # BOOK_AUTHOR = 'request_author'


class AddBookState(enum.Enum):
    INPUT_TITLE = 'input_title'
    INPUT_AUTHOR = 'input_author'
    INPUT_GENRE = 'input_genre'
    INPUT_CONDITION = 'input_condition'
    INPUT_PHOTO = 'input_photo'
    FINISH_ADD_BOOK = 'finish_add_book'


bot = TeleBot(REQUEST_BOT_TOKEN)
bot.add_custom_filter(custom_filters.StateFilter(bot))


@csrf_exempt
def webhook(request):
    data = json.loads(request.body)
    update = types.Update.de_json(data)
    bot.get_state(data['message']['from']['id'], data['message']['chat']['id'])
    print(bot.get_state(data['message']['from']['id'], data['message']['chat']['id']))
    bot.process_new_updates([update])
    return HttpResponse()


@bot.message_handler(commands=['start'])
def handle_start_command(message):
    bot.set_state(message.from_user.id, StartState.SHARE_CONTACT.value, message.chat.id)
    button = types.KeyboardButton(text='Share Phone Number', request_contact=True)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row(button)
    bot.send_message(
        message.chat.id, 
        'Please share your phone number to proceed.', 
        reply_markup=keyboard
        )


@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    phone_number = message.contact.phone_number
    save_user_phone_number(phone_number)
    bot.send_message(
        message.chat.id, 
        'Thank you for sharing your phone number!', 
        reply_markup=types.ReplyKeyboardRemove()
        )


# @bot.message_handler(state=StartState.SHARE_CONTACT.value)
# def handle_manual_phone_number(message):
#     phone_number = message.text
#     if validate_phone_number(phone_number):
#         save_user_phone_number(phone_number)
#         bot.send_message(
#             message.chat.id, 
#             'Thank you for sharing your phone number!',
#             reply_markup=types.ReplyKeyboardRemove()
#             )
#         bot.delete_state(message.from_user.id, message.chat.id)
#     else:
#         bot.send_message(message.chat.id, 'Please enter phone number in this format: 901234567')


@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.reply_to(message, "In this bot you can search and request for your favorite books.")


@bot.message_handler(commands=['cancel'])
def process_add_book(message):
    bot.delete_state(message.from_user.id, message.chat.id)
    bot.reply_to(message, "Your last operation has been canceled.")


@bot.message_handler(commands=['request'])
def handle_request_book(message):
    bot.set_state(message.from_user.id, RequestBookState.BOOK_CODE.value, message.chat.id)
    bot.reply_to(message, "Input Book's unique code")


@bot.message_handler(state=RequestBookState.BOOK_CODE.value)
def process_request_book(message):
    code = message.text
    book = request_book_from_code(code)
    if book:
        book_info = f"""
#{book.code}
# Title: {book.name}
Author: {book.author}
Genre: {book.genre}
Condition: {book.condition}
Language: {book.language}
Status: {book.status}
Description: {book.description}
"""
        bot.send_photo(message.chat.id, book.cover_photo, book_info) 
        bot.delete_state(message.from_user.id, message.chat.id)
    else:
        bot.send_message(message.chat.id, "Book with that ID not found")


@bot.message_handler(commands=['add'])
def handle_add_book(message):
    bot.set_state(message.from_user.id, AddBookState.INPUT_TITLE.value, message.chat.id)
    bot.reply_to(message, "Input title of your book")


@bot.message_handler(state=AddBookState.INPUT_TITLE.value)
def handle_add_book_title(message):
    if len(message.text) >= 1:
        book_info['title'] = message.text
        bot.set_state(message.from_user.id, AddBookState.INPUT_GENRE.value, message.chat.id)
        bot.reply_to(message, "Input author of your book")
    else:
        bot.reply_to(message, 'Book title cannot be empty')


@bot.message_handler(state=AddBookState.INPUT_GENRE.value)
def handle_add_book_author(message):
    if len(message.text) >= 1:
        book_info['author'] = message.text
        bot.set_state(message.from_user.id, AddBookState.INPUT_CONDITION.value, message.chat.id)
        bot.reply_to(message, "Choose genre of your book")
    else:
        bot.reply_to(message, 'Book genre cannot be empty')


@bot.message_handler(state=AddBookState.INPUT_CONDITION.value)
def handle_add_book_condition(message):
    if len(message.text) >= 1:
        book_info['condition'] = message.text
        bot.set_state(message.from_user.id, AddBookState.INPUT_PHOTO,message.chat.id)
        bot.reply_to(message, "Upload photo of your book.")
    else:
        bot.reply_to(message, "Choose a valid condition")
        

@bot.message_handler(content_types=['photo'])
def handle_add_book_condition(message):
    photo_id = message.photo[-1].file_id
    photo = bot.get_file(photo_id)
    book_info['photo'] = photo
    print(book_info)
    bot.set_state(message.from_user.id, AddBookState.FINISH_ADD_BOOK,message.chat.id)
    bot.send_message(message.chat.id, book_info)      
    bot.reply_to(message, "Thank you")


@bot.message_handler(state=AddBookState.FINISH_ADD_BOOK.value)
def handle_finish_book(message):
    bot.send_message(message.chat.id, book_info)      
