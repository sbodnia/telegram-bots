import telebot
import random

bot = telebot.TeleBot('TOKEN_VAR')

choices = ['rock', 'paper', 'scissors']

@bot.message_handler(commands=['play'])
def handle_play(message):
    user_choice = message.text.split(' ', 1)[-1].strip().lower()

    if user_choice in choices:
        bot_choice = random.choice(choices)
        result = determine_winner(user_choice, bot_choice)
        response = f"You chose {user_choice}.\nI chose {bot_choice}.\n{result}"
    else:
        response = "Invalid choice! Please choose rock, paper or scissors."

    bot.send_message(message.chat.id, response)

def determine_winner(user_choice, bot_choice):
    if user_choice == bot_choice:
        return "It's a tie!"
    elif (user_choice == 'rock' and bot_choice == 'scissors') or \
         (user_choice == 'paper' and bot_choice == 'rock') or \
         (user_choice == 'scissors' and bot_choice == 'paper'):
        return "Congratulations! You win!"
    else:
        return "I win! Try again."

bot.infinity_polling()