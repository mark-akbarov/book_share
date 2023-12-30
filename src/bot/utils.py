

def set_state(bot, message, state):
    bot.set_state(message.from_user.id, state=state)
    

def get_state(bot, message):
    return bot.get_state(message.from_user.id, message.chat.id)