import telebot
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone
import config

bot = telebot.TeleBot(TOKEN)

# Function: send notify
def send_reminders():
    today = datetime.now()
    if today.weekday() not in EXCLUDED_WEEKDAYS:
        if today.weekday() in [0,2] and (today.time().hour == 9 and today.time().minute == 55):
            bot.send_sticker(CHAT_ID, STICKER)
            bot.send_message(CHAT_ID, 'example 1')
        if today.weekday() in [1,4] and (today.time().hour == 9 and today.time().minute == 55):
            bot.send_sticker(CHAT_ID, STICKER)
            bot.send_message(CHAT_ID, 'example 2')
        if today.weekday() in [4] and (today.time().hour == 11 and today.time().minute == 5):
            bot.send_sticker(CHAT_ID, STICKER)
            bot.send_message(CHAT_ID, 'example 3')

# Cron
scheduler = BackgroundScheduler()
scheduler.add_job(send_reminders, 'cron', day_of_week='mon,wed,tue,fri', hour=9, minute=55, timezone=timezone('Europe/Kyiv'))
scheduler.add_job(send_reminders, 'cron', day_of_week='fri', hour=11, minute=5, timezone=timezone('Europe/Kyiv'))
scheduler.start()

if __name__ == '__main__':
    bot.infinity_polling()
