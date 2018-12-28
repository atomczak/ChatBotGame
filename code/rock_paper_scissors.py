import random
import mongodb_connection

def play_a_round(facebook_id, user_choice):
    """Function that plays a round of rock - paper - scissors.
    Accepted arguments: 'rock', 'paper', 'scissors'
    winner bot -> 0; winner player -> 1; draw =-> None"""
    choices = ['rock', 'paper', 'scissors']
    bot_choice = random.choice(choices)
    game_outcome = -1

    # establish game outcome
    if user_choice == bot_choice:
        game_outcome = None
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
        raise Exception('Function input data does not fit the assumptions. Please check doctype')

    # establish return statements and update the database
    # winner bot -> 0; winner player -> 1; draw =-> None"
    mongodb_connection.update_player_results(facebook_id, game_outcome)
    return game_outcome

