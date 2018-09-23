import random
from flask import Flask, request
from pymessenger.bot import Bot

def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

#chooses a random message to send to the user
def get_message(user_message=""):
    sample_adjectives = ["random", "generic", "fake", "artificial", "arbitrary"]
    sample_noun = ["answer", "reply", "response", "message"]
    f = "."
    if user_message != "": f=" to the message: "+str(user_message)+"'."
    return random.choice(sample_adjectives)+" "+random.choice(sample_noun)+" #"+str(random.randint(1000,10000))+f

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"
