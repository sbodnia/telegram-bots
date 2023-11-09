import sqlite3
from config import DATABASE_FILE
from datetime import datetime

def init_db():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Create table, if isn't exists
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reminders (
        id INTEGER PRIMARY KEY,
        chat_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        nickname TEXT NOT NULL,
        date DATE NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def create_reminder(chat_id, user_id, nickname, reminder_date):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO reminders (chat_id, user_id, nickname, date)
    VALUES (?, ?, ?, ?)
    ''', (chat_id, user_id, nickname, reminder_date))
    conn.commit()
    conn.close()

def get_reminders_for_today():
    today = datetime.now().strftime('%d-%m')
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT chat_id, nickname FROM reminders WHERE date = ?
    ''', (today,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_all_birthdays(chat_id):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT nickname, date FROM reminders WHERE chat_id=?", (chat_id,))
    reminders = cursor.fetchall()
    conn.close()
    return reminders

def delete_birthday(chat_id, name):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reminders WHERE chat_id=? AND nickname=?", (chat_id, name))
    conn.commit()
    conn.close()