import telebot
from telebot import types
from telegram.constants import ParseMode
from configparser import ConfigParser
import random

# Read config.ini
cfg = ConfigParser()
cfg.read('config.ini')
token = cfg['default']['BOT_TOKEN']

# Setup token
bot = telebot.TeleBot(token)

markup = types.InlineKeyboardMarkup()
markup.add(types.InlineKeyboardButton('Наші правила🫶', url='https://t.me/c/1307921278/115'))

# Jokes

@bot.message_handler(commands=['count'])
def send_count(message):
    bot.send_message(message.chat.id, f'Нарахувала стільки квіточок: {bot.get_chat_members_count(message.chat.id)}')

@bot.message_handler(commands=['start'])
def send_start(message):
    bot.send_message(message.chat.id, "Сумували? А я вже тутоньки!")

@bot.message_handler(commands=['stop'])
def send_stop(message):
    bot.send_message(message.chat.id, "Пішла фарбуватись, незабаром повернусь!")

# Greet function
def greet_user(messages):
    for message in messages:
        for new_member in message.new_chat_members:
            bot.send_message(message.chat.id, f' [{new_member.first_name}](tg://user?id={message.from_user.id}), привіт 😍\nСкільки років? Чим займаєшся? Вчишся чи працюєш?\nЩо хочеш про себе розповісти?🙄', parse_mode="Markdown", reply_markup = markup)
bot.set_update_listener(greet_user)

# Games
choices = ['камінь', 'папір', 'ножиці']

@bot.message_handler(commands=['play'])
def handle_play(message):
    user_choice = message.text.split(' ', 1)[-1].strip().lower()

    if user_choice in choices:
        bot_choice = random.choice(choices)
        result = determine_winner(user_choice, bot_choice)
        response = f"Твій вибір {user_choice}.\nЯ обрала {bot_choice}.\n{result}"
    else:
        response = "Невірний вибір! Напиши камінь, папір або ножиці."

    bot.send_message(message.chat.id, response)

# Determine the winner of the game
def determine_winner(user_choice, bot_choice):
    if user_choice == bot_choice:
        return "Нічия!"
    elif (user_choice == 'камінь' and bot_choice == 'ножиці') or \
         (user_choice == 'папір' and bot_choice == 'камінь') or \
         (user_choice == 'ножиці' and bot_choice == 'папір'):
        return "Твоя взяла! Грац!"
    else:
        return "Ха! А я переможець!"

# Run in main
if __name__ == '__main__':
	bot.infinity_polling()

