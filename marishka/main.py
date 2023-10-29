import telebot
from telegram.constants import ParseMode
from configparser import ConfigParser

# Read config.ini
cfg = ConfigParser()
cfg.read('config.ini')
token = cfg['default']['BOT_TOKEN']

# Setup token
bot = telebot.TeleBot(token)

# Greet function
def greet_user(messages):
    for message in messages:
        for new_member in message.new_chat_members:
            bot.send_message(message.chat.id, f' [{new_member.first_name}](tg://user?id={message.from_user.id}), привіт.\nСкільки років? Чим займаєшся? Вчишся чи працюєш?\nЩо хочеш про себе розповісти?', parse_mode="Markdown")
bot.set_update_listener(greet_user)

# Run in main
if __name__ == '__main__':
	bot.infinity_polling()

