from telebot import types

from book.models.book import Genre, Language, Condition


class KeyboardMarkup:
    def __init__(self, buttons: list, *args, **kwargs) -> None:
        self.buttons = buttons

    def create(self, *args, **kwargs):
        if len(self.buttons) > 1:    
            buttons = [types.KeyboardButton(text=state, **kwargs) for state in self.buttons]
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            keyboard_layout = keyboard.row(*buttons)
        else:
            buttons = types.KeyboardButton(text=self.buttons[0], **kwargs)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            keyboard_layout = keyboard.row(buttons)
        return keyboard_layout
    
    def create_sliced(self, rows):
        buttons = [types.KeyboardButton(text=state) for state in self.buttons]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard_layout = keyboard.row(*buttons[:len(buttons)//rows])
        keyboard_layout = keyboard.row(*buttons[len(buttons)//rows:])
        return keyboard_layout


yes_no_markup = KeyboardMarkup(['Yes, proceed', 'No, change details'])

share_markup = KeyboardMarkup(['Share Contact'], request_contact=True)

genre_markup = KeyboardMarkup(Genre)

condition_markup = KeyboardMarkup(Condition)

language_markup = KeyboardMarkup(Language)