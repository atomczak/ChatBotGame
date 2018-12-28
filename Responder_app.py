#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request
from code.helpers import *
import json

#initiate the web app
app = Flask(__name__)

#We will receive messages that Facebook sends to our bot at this endpoint:
@app.route("/", methods=['GET', 'POST'])

def receive_message():
    if request.method == 'GET':             # if type is 'GET' it means FB wants to verify tokens
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    else:                                   # if type is not 'GET' it must be 'POST' - we have a message
        user_message = request.get_json()   # read message as json
        handle_messages(user_message)       # process the message and respond
        print("")
    return "Message Processed"

#If the program (Responder_app.py) is executed (double-clicked), it will set name to main, thus run app:
if __name__ == "__main__":
    app.run()
