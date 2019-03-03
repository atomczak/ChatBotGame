import random
from code import mysql_connection as db
from code.fb_messenger import *
from code import bot_behaviour
from time import sleep
from Responder_app import database
import logging
import os
log = logging.getLogger(os.path.basename(__file__))

def play_a_round(userid, user_choice):
    """Function that plays a round of rock - paper - scissors.
    Accepted arguments: 'rock', 'paper', 'scissors'
    winner bot -> 0; winner player -> 1; draw =-> None"""
    choices = ['rock', 'paper', 'scissors']
    bot_choice = random.choice(choices)
    log.info("User chose: '" + user_choice + "', Bot chose: '" + bot_choice + "'")
    game_outcome = -1
    # establish game outcome
    if user_choice == bot_choice:
        game_outcome = -1
    elif user_choice == 'rock':
        if bot_choice == 'paper':
            game_outcome = 0
        else:
            game_outcome = 1
    elif user_choice == 'paper':
        if bot_choice == 'scissors':
            game_outcome = 0
        else:
            game_outcome = 1
    elif user_choice == 'scissors':
        if bot_choice == 'rock':
            game_outcome = 0
        else:
            game_outcome = 1
    else:
        pass
        #raise Exception('Function input data does not fit the assumptions. Please check doctype')

    # establish return statements and update the database
    # winner bot -> 0; winner player -> 1; draw =-> -1"
    if database: db.update_player_results(userid, game_outcome)
    return [game_outcome, bot_choice]

def play(user_message = "", userid="", bot=""):
    rps_pattern = {
        "new_game" : [r'start', r'play', r'game'],
        "rock" :  [r'rock', r'✊'],
        "paper" :  [r'paper', r'✋'],
        "scissors" :  [r'scissors', r'✌']
    }
    choice = bot_behaviour.regex_pattern_matcher(user_message, pat_dic=rps_pattern)
    log.info(choice)
    if database: db.add_conversation(userid, 'User', choice)

    if choice == "new_game":
        entry_message = random.choice(["Which one do you choose?", "so, rock, paper or scissors?", "ok, let's play!"])
        bot.fb_send_quick_replies(userid, entry_message, ["✊ rock","✋ paper","✌ scissors"])
        if database:
            db.add_conversation(userid, 'Bot', entry_message)
        log.info("User #{0} started a new RPS game with: '{1}'.".format(str(userid)[0:4], str(user_message)))
        return "Game started"
    elif choice == "rock" or choice == "paper" or choice == "scissors":
        log.info("User chose: "+str(choice))
        game_outcome = play_a_round(userid, choice)
        if game_outcome[0] == -1:
            response = random.choice(["Uff! It's a draw!", "Tie!"])
        elif game_outcome[0] == 0:
            response = random.choice(["Hah! I won!", "I'm just lucky :)"])
        elif game_outcome[0] == 1:
            response = random.choice(["Damm! I lost!", "You win!"])
        else:
            response = "I can't play this game."
        bot.fb_send_text_message(userid, game_outcome[1])
        if database: db.add_conversation(userid, 'Bot', game_outcome[1])
        sleep(0.2)
        bot.fb_send_text_message(userid, str(response))
        if database: db.add_conversation(userid, 'Bot', str(response))
        sleep(0.4)
        bot.fb_send_quick_replies(userid, "Another round?", ["✊ rock","✋ paper","✌ scissors"])
        if database: db.add_conversation(userid, 'Bot', "Another round?")
        return "Game played"
    else:
        return "Error?"
