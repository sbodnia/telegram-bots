import telebot

bot = telebot.TeleBot('TOKEN_VAR')

@bot.message_handler(commands=['start', 'info'])
def main(message):
    bot.send_message(message.chat.id, f'▪️ First Name: {message.from_user.first_name}\n▪️ Last Name: {message.from_user.last_name}\n▪️ Username: {message.from_user.username}\n▪️ ID: {message.from_user.id}\n▪️ Language code: {message.from_user.language_code}') 

bot.infinity_polling()