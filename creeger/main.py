import telebot
from telebot import types
import webbrowser

bot = telebot.TeleBot('6258011227:AAGUia3xAyAMdLEvCjg8uxvfVDjN97OCiBE')

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, 'hello')

@bot.message_handler(commands=['info'])
def main(message):
    webbrowser.open('https://getemoji.com/')

@bot.message_handler(commands=['last'])
def main(message):
    bot.send_message(message.chat.id, f'▪️ First Name: {message.from_user.first_name}\n▪️ Last Name: {message.from_user.last_name}\n▪️ Username: {message.from_user.username}\n▪️ ID: {message.from_user.id}\n▪️ Language code: {message.from_user.language_code}')

@bot.message_handler(commands=['help'])
def main(message):
    bot.send_message(message.chat.id, '<b>bot v help</b>', parse_mode='html')

@bot.message_handler(content_types=['photo'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Google', url='google.com'))
    bot.reply_to(message, 'WOW!', reply_markup = markup)

@bot.message_handler()
def info(message):
    if message.text.lower() == 'qqq':
        bot.send_message(message.chat.id, 'sasa')    

bot.infinity_polling() #same of bot.polling(none_stop=True)