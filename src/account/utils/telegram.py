import telebot
from core.settings import REQUEST_BOT_TOKEN

bot = telebot.TeleBot(REQUEST_BOT_TOKEN)

@bot.message_handler(['start'])
def handle_message(message):
    print(message)
    bot.reply_to(message, "Welcome to Share Book Bot. Here you can share your books \
        or requuest books from other users.")