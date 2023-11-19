import telebot
from datetime import datetime
import database
from config import TOKEN, TIMEZONE
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone
from database import get_all_birthdays

bot = telebot.TeleBot(TOKEN)

# Initialization database
database.init_db()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привіт, котику!🥰\nЯ бот, яка може допомогти тобі запамʼятати Дні Народження у нашому чатику!😘\n\nДля встановлення нагадування треба запустити наступну команду\n\n команду /add DD-MM nickname 😊\n\nА також ти можеш дізнатися усі записи про Дні Народження цього чатику за допомогою команди /all")

# Function: add new birthday
@bot.message_handler(commands=['add'])
def handle_reminder(message):
    try:
        _, date_str, nickname = message.text.split()
        # Parse date and add notify to database
        database.create_reminder(message.chat.id, message.from_user.id, nickname, date_str)
        bot.reply_to(message, "Нагадування встановлено!😎")
    except Exception as e:
        bot.reply_to(message, "Помилочка сталася!😱\nВикористовуй формат: /add DD-MM nickname")

# Function: send notify
def send_reminders():
    for chat_id, nickname in database.get_reminders_for_today():
        bot.send_message(chat_id, f"Вауууу!🤩🤩🤩\nСьогодні День Народження у нашого котика {nickname}!🥳\nВітаємо усім чатиком! 🎉")

# Function: get all birthdates
@bot.message_handler(commands=['all'])
def send_all_birthdays(message):
    chat_id = message.chat.id
    birthdays_list = get_all_birthdays(chat_id)
    response = "Усі Дні Народження:\n\n"
    for name, date in birthdays_list:
        response += f"🎂 {name}: {date}\n"
    bot.send_message(message.chat.id, response)

# Function: delete birthdate
@bot.message_handler(commands=['delete'])
def handle_delete_birthday(message):
    try:
        _, name = message.text.split(maxsplit=1)
        chat_id = message.chat.id
        database.delete_birthday(chat_id, name)
        bot.reply_to(message, f"День Народження {name} видалено😓")
    except ValueError:
        bot.reply_to(message, "Покажи мені кого треба видалити із записів командою у форматі\n/delete nickname")
    except Exception as e:
        bot.reply_to(message, f"Помилочка сталася!😱: {e}")

# Cron
scheduler = BackgroundScheduler()
scheduler.add_job(send_reminders, 'cron', hour=10, timezone=timezone(TIMEZONE))
scheduler.add_job(send_reminders, 'cron', hour=12, timezone=timezone(TIMEZONE))
scheduler.start()

if __name__ == '__main__':
    bot.infinity_polling()
