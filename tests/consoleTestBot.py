"""
Use this command line bot to test bot conversational abilities
It does not use NLP (yet).
"""
import random
import json
import sys
sys.path.append('..')
from code import bot_behaviour
import logging
import os
log = logging.getLogger(os.path.basename(__file__))

print("")
print(" --- beginning of the new conversation (say 'bye' to exit) --- ")
print("")

while True:
    userAns = input("YOU: ")
    userAns = userAns.lower()
    if "bye" in userAns:
        print("BOT: goodbye :)")
        print("")
        print(" --- end of the conversation --- ")
        print("")
        break
    else:
        entity = best_match_entity(userAns)
        response = bot_response(userAns, entity)    #second argument would be the entity
        print("BOT: " + response)
