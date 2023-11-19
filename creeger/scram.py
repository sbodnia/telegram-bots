import telebot
from telegram.ext import Updater, CallbackContext
bot = telebot.TeleBot('6258011227:AAGUia3xAyAMdLEvCjg8uxvfVDjN97OCiBE')
updater = Updater(token='6258011227:AAGUia3xAyAMdLEvCjg8uxvfVDjN97OCiBE', use_context=True)
# @bot.message_handler(commands=['start'])
# def main(message):
#     bot.send_message(message.chat.id, 'hello')
j = updater.job_queue

def morning(context: CallbackContext):
    message = "Good Morning! Have a nice day!"
    context.bot.send_message(chat_id=id, text=message)

job_daily = j.run_daily(morning, days=(0, 1, 2, 3, 4, 5, 6), time=datetime.time(hour=8, minute=21, second=00))

bot.infinity_polling()