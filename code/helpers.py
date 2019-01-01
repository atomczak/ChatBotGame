#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
In this code are functions for basic bot behaviours.

"""

import re
import random

import json
from difflib import get_close_matches
#import tokens
from code import rock_paper_scissors as rps
from code import tokens
from code import mongodb_connection as mng
from code.resources import *
from code.pymessenger.bot import Bot
#from pymessenger.bot import Bot
from flask import Flask, request
from datetime import date
from time import sleep

#initiate the pymessenger bot object
bot = Bot(tokens.fb_access)

#fetch user ids from the DB:
users = []
for user in mng.Player.objects():
    users.append(user.facebook_id)

#take token sent by facebook and verify if it matches:
def verify_fb_token(token_sent):
    if token_sent == tokens.fb_verification:
        return request.args.get("hub.challenge")
        print("[LOG-VERI] Token verification succesfull.")
    else:
        print("[LOG-VERI] Failed to verify token.")
    return 'Invalid verification token'

def handle_messages(user_message):
    for event in user_message['entry']:
        messaging = event['messaging']
        for message in messaging:
            uid = message['sender']['id']   #sender, thus our recipient id
            if message.get('message'):
                mark_seen(uid)
                add_new_user(uid)
                #Facebook Messenger ID for user so we know where to send response back to
                msg = message['message']
                if int(uid) != int(tokens.fb_bot_id):
                    fake_typing(uid, 1)
                    #bot.get_user_info(uid)
                    if msg.get('text'):
                        handle_text(msg, uid)
                    elif msg.get('sticker_id'):
                        handle_sticker(msg, uid)
                    elif msg.get('attachments'):
                        handle_attachment(msg, uid)
            elif message.get('delivery'):
                print("[LOG-DELI] Message from #{0} delivered to #{1}.".format(str(uid)[0:4], str(message['recipient']['id'])[0:4]))
            elif message.get('read'):
                print("[LOG-SEEN] Message from #{0} read by #{1}.".format(str(uid)[0:4], str(message['recipient']['id'])[0:4]))

def add_new_user(user_id):
    if user_id not in users:    # add new user
        #get_user_info(bot,uid)  #first_name TODO
        mng.create_player(user_id)
        users.append(user_id)
    else:                       # user already in the DB - collect info
        mng.find_player(user_id).first_name
        #TODO

# react when the user sends some text
def handle_text(msg, uid):
    text = msg.get('text')
    mng.add_conversation(uid, 'User', text)
    if text == "start":
        send_quick_replies(uid)
        print("[LOG-MESG] User #{0} said secret word: '{1}' and I tried to answer with quick replies.".format(str(uid)[0:4], str(msg.get('text'))))
    elif text == "✊ rock" or text == "✋ paper" or text == "✌ scissors":
        print("[LOG-MESG] User #{0} said secret word: '{1}' and I tried to start a game.".format(str(uid)[0:4], str(msg.get('text'))))
        game_outcome = rps.play_a_round(uid,text)
        if game_outcome[0] is None:
            response = """Uff! It's a draw!"""
        elif game_outcome[0] == 0:
            response = "Hah! I won!"
        elif game_outcome[0] == 1:
            response = "Damm! I lost!"
        send_message(uid, game_outcome[1])
        mng.add_conversation(uid, 'Bot', game_outcome[1])
        send_message(uid, str(response))
        mng.add_conversation(uid, 'Bot', str(response))
        send_quick_replies(uid)
    else:
        entity = best_match_entity(msg)
        print("[LOG-MESG] User #{0} said: '{1}' and I recognize it as: {2}.".format(str(uid)[0:4], str(msg.get('text')), entity))
        response = bot_response(text, entity)
        send_message(uid, response)
        mng.add_conversation(uid,'Bot',response)

#react when the user sends a sticker
def handle_sticker(msg, uid):
    print("[LOG-MESG] User #{0} sent a sticker.".format(str(uid)[0:4]))
    response = recognize_sticker(str(msg.get('sticker_id')))
    send_message(uid, response)
    mng.add_conversation(uid,'User','Some sticker')     # True=human, False=bot
    mng.add_conversation(uid,'Bot',response)           # True=human, False=bot

#react when the user sends a GIFs, photos, videos, or any other non-text item:
def handle_attachment(msg, uid):
    print("[LOG-MESG] User #{0} sent a gif.".format(str(uid)[0:4]))
    #Send funny gif:
    image_url = r'https://media.giphy.com/media/L7ONYIPYXyc8/giphy.gif'
    send_image(uid, image_url)
    mng.add_conversation(uid,'User','Some attachment (GIF)')     # True=human, False=bot
    mng.add_conversation(uid,'Bot','GIF with a guy.')           # True=human, False=bot

def send_message(recipient_id, response):
    if type(response) == list: response = random.choice(response)
    bot.send_text_message(recipient_id, response)
    print("[LOG-RESP] Bot has answered: '" + str(response) + "'.")

def send_image(recipient_id, image_url):
    bot.send_image_url(recipient_id, image_url)
    #local file:
    #bot.send_image(recipient_id, r'C:\Users\Artur\Desktop\CODE\Chatbot Game\resources\CogitoErgoSum.jpg')
    print("[LOG-RESP] Bot has answered with a funny picture.")

def send_quick_replies(recipient_id):
    reply_message = "So, rock, paper or scissors?"
    mng.add_conversation(recipient_id, 'Bot', reply_message)
    #reply_options = (["one","@one"],["two","@two"])
    #reply_options=[{"content_type":"text","title":"Search","payload"<POSTBACK_PAYLOAD>","image_url":"http://example.com/img/red.png"},{"content_type":"location"}]
    reply_options = [{"content_type":"text","title":"✊ rock","payload":"<POSTBACK_PAYLOAD>"},
        {"content_type":"text","title":"✋ paper","payload":"<POSTBACK_PAYLOAD>"},
        {"content_type":"text","title":"✌ scissors","payload":"<POSTBACK_PAYLOAD>"}]
    #bot.send_quickreply(recipient_id,reply_message,reply_options)
    bot.send_quick_replies_message(recipient_id, reply_message, reply_options)
    print("[LOG-RESP] Bot has answered with options.")

def mark_seen(recipient_id):
    bot.send_action(recipient_id, 'mark_seen')

def fake_typing(recipient_id, duration=2):
    sleep(duration/2)
    bot.send_action(recipient_id, 'typing_on')
    sleep(duration)
    bot.send_action(recipient_id, 'typing_off')

#Prepare an answer, based on the user message:
def bot_response(userAns, entity=""):
    if entity == "" or entity is None:
        entity = regex_pattern_matcher(userAns)   #no entity from NLP so try to find with regex
    response = responder(entity, userAns)   #prepare the response based on the entity given
    if type(response) == list:
        response = random.choice(response)
    return response

def time(message):
    timestamp = float(message['timestamp'])/1000
    return date.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

#Regular Expression pattern finder that searches for intents from patternDictionary:
def regex_pattern_matcher(str):
    intent = False
    search_object = False
    for key, value in pattern_dictionary.items():
        if type(value) == list:
            for v in value:
                s = re.search(v, str, re.M|re.I|re.U)    #|re.U
                if s: search_object = s
        else:
            search_object = re.search(value, str, re.M|re.I|re.U)    #|re.U
        if search_object: intent = key   #cause found searchObj.group()
    return intent

def best_match_entity(message):
    try:
        entities = list(message['message'].get('nlp').get('entities').keys())
        #entities.remove("sentiment")
        confidence = []
        for c in list(message['message'].get('nlp').get('entities').values()):
            confidence.append(c[0]['confidence'])
        # create dictionary entity:confidence:
        iterable = zip(entities, confidence)
        pairs = {key: value for (key, value) in iterable}
        best_match = max(pairs, key=pairs.get)
        print("[LOG-ENTY] Recognized entities: {0}, best is: '{1}'.".format(str(pairs), best_match))
        return best_match
    except:
        return None

#Lookup the definition of the word in the dictionary:
def translate(word):
    encyclopedia = json.load(open("../resources/Encyclopedia.json"))    #TODO moze lepiej zeby takie rzeczy się otwierało raz - przy starcie apki?
    word = word.lower()
    if word in encyclopedia:
        return encyclopedia[word]
    elif len(get_close_matches(word, encyclopedia.keys())) > 0:
        return ["CloseMatch", encyclopedia[get_close_matches(word, encyclopedia.keys())[0]], encyclopedia[get_close_matches(w, encyclopedia.keys())[1]]]
