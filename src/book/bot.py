import enum
import json

from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from telebot import TeleBot, types, custom_filters

from core.utils.validations import validate_phone_number
from core.settings import REQUEST_BOT_TOKEN, GROUP_CHAT_ID

from book.models.book import Book, Condition, Genre, Language, AvailabilityStatus
# from book.serializers.book import BookCreateSerializer
from book.utils import save_user_phone_number, request_book_from_code, add_book_to_db, generate_unique_code


class KeyboardMarkup:
    def __init__(self, button_names: list) -> None:
        self.button_names = button_names

    def create(self):
        buttons = [types.KeyboardButton(text=state) for state in self.button_names]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard_layout = keyboard.row(*buttons)
        return keyboard_layout
    

# Genre Buttons
genre_buttons = [types.KeyboardButton(text=state) for state in Genre]
genre_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
genre_keyboards = genre_keyboard.row(*genre_buttons)

# Condition Buttons
condition_buttons = [types.KeyboardButton(text=state) for state in Condition]
condition_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
condition_keyboards = condition_keyboard.row(*condition_buttons[:len(condition_buttons)//2])
condition_keyboards = condition_keyboard.row(*condition_buttons[len(condition_buttons)//2:])

# Language Buttons
language_buttons = [types.KeyboardButton(text=state) for state in Language]
language_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
language_keyboards = language_keyboard.row(*language_buttons)

# Yes-No Buttons
yes_button = types.KeyboardButton(text='Yes, proceed')
no_button = types.KeyboardButton(text='No, change details')
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
yes_no_markup = keyboard.row(yes_button, no_button)


book_info = {}


class StartState(enum.Enum):
    SHARE_CONTACT = 'Share Contact'

    
class RequestBookState(enum.Enum):
    BOOK_CODE = 'Request Code'
    # BOOK_TITLE = 'request_title'
    # BOOK_AUTHOR = 'request_author'


class AddBookState(enum.Enum):
    INPUT_TITLE = 'Title'
    INPUT_AUTHOR = 'Author'
    INPUT_GENRE = 'Genre'
    INPUT_CONDITION = 'Condition'
    INPUT_PHOTO = 'Photo'
    INPUT_LANGUAGE = 'Language'
    


bot = TeleBot(REQUEST_BOT_TOKEN)
bot.add_custom_filter(custom_filters.StateFilter(bot))


@csrf_exempt
def webhook(request):
    data = json.loads(request.body)
    update = types.Update.de_json(data)
    bot.get_state(data['message']['from']['id'], data['message']['chat']['id'])
    print(book_info)
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


@bot.message_handler(content_types=['contact'], state=StartState.SHARE_CONTACT.value)
def handle_contact(message):
    phone_number = message.contact.phone_number
    bot.delete_state(message.from_user.id, message.chat.id)
    bot.send_message(
        message.chat.id, 
        'Thank you for sharing your phone number!', 
        reply_markup=types.ReplyKeyboardRemove()
        )
    save_user_phone_number(phone_number)


@bot.message_handler(state=StartState.SHARE_CONTACT.value)
def handle_manual_phone_number(message):
    phone_number = message.text
    if validate_phone_number(phone_number):
        bot.send_message(
            message.chat.id, 
            'Thank you for sharing your phone number!',
            reply_markup=types.ReplyKeyboardRemove()
            )
        bot.delete_state(message.from_user.id, message.chat.id)
        save_user_phone_number(phone_number)
    else:
        bot.send_message(message.chat.id, 'Please enter phone number in this format: 901234567')


@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.reply_to(message, "In this bot you can search and request for your favorite books.")


@bot.message_handler(commands=['cancel'])
def process_cancel(message):
    bot.delete_state(message.from_user.id, message.chat.id)
    bot.reply_to(message, "Your operation has been canceled.")


@bot.message_handler(commands=['request'])
def handle_request_book(message):
    bot.reply_to(message, "Input Book's unique code")
    bot.set_state(message.from_user.id, RequestBookState.BOOK_CODE.value, message.chat.id)


@bot.message_handler(state=RequestBookState.BOOK_CODE.value)
def process_request_book(message):
    code = message.text
    book = request_book_from_code(code)
    
    book_info = f"""
#{book.code}
Title: {book.title}
Author: {book.author}
Genre: {book.genre}
Condition: {book.condition}
Language: {book.language}
Status: {book.status}
Description: {book.description}
"""
    if book is None:
        bot.reply_to(message, "Book with that ID not found")
    elif book is not None:
        bot.send_photo(message.chat.id, book.cover_photo, book_info) 
        bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(commands=['add'])
def handle_add_book(message):
    bot.set_state(message.from_user.id, AddBookState.INPUT_TITLE.value, message.chat.id)
    bot.reply_to(message, "Input title of your book")


@bot.message_handler(state=AddBookState.INPUT_TITLE.value)
def handle_add_book_title(message):
    if len(message.text) >= 1:
        book_info['title'] = message.text
        bot.set_state(message.from_user.id, AddBookState.INPUT_AUTHOR.value, message.chat.id)
        bot.reply_to(message, "Input author of your book")
    else:
        bot.reply_to(message, 'Book title cannot be empty')


@bot.message_handler(state=AddBookState.INPUT_AUTHOR.value)
def handle_add_book_author(message):
    if len(message.text) >= 1:
        bot.set_state(message.from_user.id, AddBookState.INPUT_GENRE.value, message.chat.id)
        bot.reply_to(message, "Input genre of your book:", reply_markup=genre_keyboards)
        book_info['author'] = message.text
    else:
        bot.reply_to(message, 'Book author cannot be empty')


@bot.message_handler(state=AddBookState.INPUT_GENRE.value)
def handle_add_book_genre(message):
    if message.text in Genre:
        bot.send_message(
            chat_id=message.chat.id,  
            text="Choose condition of your book:", 
            reply_to_message_id=message.message_id,
            reply_markup=condition_keyboards
            )
        bot.set_state(message.from_user.id, AddBookState.INPUT_CONDITION.value, message.chat.id)
        book_info['genre'] = message.text
    else:
        bot.reply_to(message, 'Please choose genre from below')
        

@bot.message_handler(state=AddBookState.INPUT_CONDITION.value)
def handle_add_book_condition(message):
    if message.text in Condition:
        bot.send_message(
            chat_id=message.chat.id,  
            text="Choose language of your book:", 
            reply_to_message_id=message.message_id,
            reply_markup=language_keyboards
            )
        bot.set_state(message.from_user.id, AddBookState.INPUT_LANGUAGE.value, message.chat.id)
        book_info['condition'] = message.text
    else:
        bot.reply_to(message, 'Please choose condition from below')


@bot.message_handler(state=AddBookState.INPUT_LANGUAGE.value)
def handle_add_book_language(message):
    if message.text in Language:
        bot.send_message(
            chat_id=message.chat.id,  
            text="Upload photo of the book:", 
            reply_to_message_id=message.message_id,
            )
        bot.set_state(message.from_user.id, AddBookState.INPUT_PHOTO.value, message.chat.id)
        book_info['language'] = message.text
    else:
        bot.reply_to(message, 'Please choose language from below')


@bot.message_handler(content_types=['photo'], state=AddBookState.INPUT_PHOTO.value)
def handle_add_book_photo(message):
    if message.content_type != 'photo':
        bot.reply_to(message, "Please send a photo file of the book's cover.")
    
    photo_id = message.photo[-1].file_id
    book_info['telegram_photo_id'] = photo_id
    bot.reply_to(message, "Please check below information for correctness!")
    
    title = book_info['title']
    author = book_info['author']
    genre = book_info['genre']
    condition  = book_info['condition']
    language = book_info['language']
    photo = book_info['telegram_photo_id']
    book = f"""
Title: {title}
Author: {author}
Genre: {genre}
Condition: {condition}
Language: {language}
"""
    bot.set_state(message.from_user.id, 'Finish book', message.chat.id)
    bot.send_photo(message.chat.id, photo=photo, caption=book, reply_markup=yes_no_markup)
    

@bot.message_handler(state='Finish book')
def handle_confirmation(message):
    if message.text == 'Yes, proceed':
        bot.send_message(message.chat.id, 'Your book details have been saved!')
        bot.delete_state(message.from_user.id, message.chat.id)
        book = Book(
            shared_by_telegram_user=message.from_user.id, 
            code=generate_unique_code(), 
            status=AvailabilityStatus.AVAILABLE, 
            **book_info
            )
        book.save()
    elif message.text == 'No, change details':
        choices = KeyboardMarkup(AddBookState)
        keyboard_markup = choices.create()
        bot.send_message(
            message.chat.id, 
            'What would you like to change?', 
            reply_markup=keyboard_markup
            )
    