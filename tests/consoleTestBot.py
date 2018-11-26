"""
Use this command line bot to test bot conversational abilities
"""

import random
import json
import sys
sys.path.append('../code')
from helpers import *

#response = random.choice(response)

print(" --- beginning of the new conversation (say 'bye' to exit) --- ")

while True:
    userAns = input("YOU: ")
    userAns = userAns.lower()
    if "bye" in userAns:
        print("BOT: goodbye :)")
        print(" --- end of the conversation --- ")
        break
    else:
        response = botResponse(userAns, "")    #second argument would be the entity
        print("BOT: " + response)
