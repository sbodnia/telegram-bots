import telebot

TOKEN = '6258011227:AAGUia3xAyAMdLEvCjg8uxvfVDjN97OCiBE'
bot = telebot.TeleBot(TOKEN)

# main func
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Ok")

bot.infinity_polling()
