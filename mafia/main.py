import telebot
import random
 
bot = telebot.TeleBot("6258011227:AAGUia3xAyAMdLEvCjg8uxvfVDjN97OCiBE")
admin_id = "5240519031"
players = {}
game_started = False
 
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Welcome to the Mafia game!")
 
@bot.message_handler(commands=['create'])
def create_game(message):
    if str(message.from_user.id) != admin_id:
        bot.reply_to(message, "Only the admin can create a game.")
        return
 
    if game_started:
        bot.reply_to(message, "A game is already in progress.")
        return
 
    try:
        command, num_players, num_mafia = message.text.split()
        num_players = int(num_players)
        num_mafia = int(num_mafia)
    except ValueError:
        bot.reply_to(message, "Invalid command format. Use /create <num_players> <num_mafia>.")
        return
 
    players.clear()
    for i in range(1, num_players + 1):
        players[i] = {
            'nickname': '',
            'role': '',
            'subrole': ''
        }
 
    bot.reply_to(message, f"A new game has been created with {num_players} players and {num_mafia} mafia.")
 
@bot.message_handler(commands=['register'])
def register_player(message):
    player_id = str(message.from_user.id)
    if player_id in players:
        bot.reply_to(message, "You are already registered.")
        return
 
    if not game_started:
        bot.reply_to(message, "No game has been created yet.")
        return
 
    nickname = message.text.split()[1]
    players[player_id]['nickname'] = nickname
 
    bot.reply_to(message, f"You have been registered as {nickname}. Your player number is {player_id}.")
 
@bot.message_handler(commands=['go'])
def start_game(message):
    if str(message.from_user.id) != admin_id:
        bot.reply_to(message, "Only the admin can start the game.")
        return
 
    if game_started:
        bot.reply_to(message, "The game has already started.")
        return
 
    num_players = len(players)
    num_mafia = sum(1 for player in players.values() if player['role'] == 'mafia')
 
    if num_players == 0 or num_mafia == 0:
        bot.reply_to(message, "Not enough players or mafia to start the game.")
        return
 
    mafia_players = random.sample(players.keys(), num_mafia)
    don_player = random.choice(mafia_players)
    sheriff_player = random.choice(list(set(players.keys()) - set(mafia_players)))
 
    for player_id, player in players.items():
        if player_id in mafia_players:
            player['role'] = 'mafia'
            if player_id == don_player:
                player['subrole'] = 'don'
        elif player_id == sheriff_player:
            player['role'] = 'sheriff'
        else:
            player['role'] = 'civilian'
 
        role_message = f"You are a {player['role']}"
        if player['subrole']:
            role_message += f" ({player['subrole']})"
        bot.send_message(player_id, role_message)
 
    bot.reply_to(message, "The game has started. Roles have been assigned to the players.")
 
@bot.message_handler(commands=['gon'])
def night_phase(message):
    if str(message.from_user.id) != admin_id:
        bot.reply_to(message, "Only the admin can start the night phase.")
        return
 
    if not game_started:
        bot.reply_to(message, "No game has been created yet.")
        return
 
    for player_id, player in players.items():
        if player['role'] == 'mafia':
            bot.send_message(player_id, "It's night. Use /kill <player_number> to eliminate a player.")
        elif player['role'] == 'sheriff':
            bot.send_message(player_id, "It's night. Use /detect <player_number> to investigate a player.")
 
    bot.reply_to(message, "Night phase has started. Mafia and Sheriff can use their commands.")
 
@bot.message_handler(commands=['kill'])
def kill_player(message):
    player_id = str(message.from_user.id)
    if players[player_id]['role'] != 'mafia':
        bot.reply_to(message, "Only mafia can use the kill command.")
        return
 
    try:
        command, target_player = message.text.split()
        target_player = int(target_player)
    except ValueError:
        bot.reply_to(message, "Invalid command format. Use /kill <player_number>.")
        return
 
    if target_player not in players:
        bot.reply_to(message, "Invalid player number.")
        return
 
    del players[target_player]
    bot.reply_to(message, f"Player {target_player} has been eliminated.")
 
@bot.message_handler(commands=['detect'])
def detect_player(message):
    player_id = str(message.from_user.id)
    if players[player_id]['role'] != 'sheriff':
        bot.reply_to(message, "Only the sheriff can use the detect command.")
        return
 
    try:
        command, target_player = message.text.split()
        target_player = int(target_player)
    except ValueError:
        bot.reply_to(message, "Invalid command format. Use /detect <player_number>.")
        return
 
    if target_player not in players:
        bot.reply_to(message, "Invalid player number.")
        return
 
    if players[target_player]['role'] == 'mafia':
        bot.reply_to(message, f"Player {target_player} is a mafia.")
    else:
        bot.reply_to(message, f"Player {target_player} is not a mafia.")
 
@bot.message_handler(commands=['god'])
def lynching_phase(message):
    if str(message.from_user.id) != admin_id:
        bot.reply_to(message, "Only the admin can start the lynching phase.")
        return
 
    if not game_started:
        bot.reply_to(message, "No game has been created yet.")
        return
 
    for player_id, player in players.items():
        if player_id != admin_id:
            bot.send_message(player_id, "It's lynching phase. Use /lynch <player_number> to vote for a player.")
 
    bot.reply_to(message, "Lynching phase has started. Players can use the lynch command.")
 
@bot.message_handler(commands=['lynch'])
def lynch_player(message):
    player_id = str(message.from_user.id)
    if player_id == admin_id:
        bot.reply_to(message, "The admin cannot vote.")
        return
 
    try:
        command, target_player = message.text.split()
        target_player = int(target_player)
    except ValueError:
        bot.reply_to(message, "Invalid command format. Use /lynch <player_number>.")
        return
 
    if target_player not in players:
        bot.reply_to(message, "Invalid player number.")
        return
 
    # Count votes
    votes = {}
    for player in players.values():
        if player['role'] != 'civilian' or player_id == target_player:
            continue
 
        if player_id not in votes:
            votes[player_id] = []
 
        votes[player_id].append(target_player)
 
    # Find player with the most votes
    max_votes = 0
    lynched_player = None
    for voter, targets in votes.items():
        num_votes = len(targets)
        if num_votes > max_votes:
            max_votes = num_votes
            lynched_player = targets[0]
 
    if lynched_player:
        del players[lynched_player]
        bot.reply_to(message, f"Player {lynched_player} has been lynched.")
    else:
        bot.reply_to(message, "No player has been lynched.")
 
@bot.message_handler(commands=['finish'])
def finish_game(message):
    if str(message.from_user.id) != admin_id:
        bot.reply_to(message, "Only the admin can finish the game.")
        return
 
    players.clear()
    game_started = False
    bot.reply_to(message, "The game has been finished.")
 
@bot.message_handler(commands=['list'])
def list_players(message):
    if str(message.from_user.id) != admin_id:
        bot.reply_to(message, "Only the admin can view the player list.")
        return
 
    player_list = ""
    for player_id, player in players.items():
        player_list += f"Player {player_id}: {player['nickname']} - Role: {player['role']}"
        if player['subrole']:
            player_list += f" ({player['subrole']})"
        player_list += "\n"
 
    bot.reply_to(message, player_list)
 
bot.polling()