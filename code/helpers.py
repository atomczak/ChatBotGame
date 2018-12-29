#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
In this code are functions for basic bot behaviours.

"""

import re
import random
from pymessenger.bot import Bot
import json
from difflib import get_close_matches
#from code import tokens
import tokens
from flask import Flask, request
from datetime import date
from resources import *
from time import sleep

#initiate the pymessenger bot object
bot = Bot(tokens.access)

#take token sent by facebook and verify if it matches:
def verify_fb_token(token_sent):
    if token_sent == tokens.verification:
        return request.args.get("hub.challenge")
        print("[LOG-VERI] Token verification succesfull.")
    else:
        print("[LOG-VERI] Failed to verify token.")
    return 'Invalid verification token'

def handle_messages(user_message):
    for event in user_message['entry']:
        messaging = event['messaging']
        for message in messaging:
            uid = message['sender']['id']   #recipient id
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                msg = message['message']
                if int(uid) != int(tokens.bot_id):
                    fake_typing(uid, 3)
                    get_user_info(uid)
                    if msg.get('text'):
                        handle_text(msg, uid)
                    elif msg.get('sticker_id'):
                        handle_sticker(msg, uid)
                    elif msg.get('attachments'):
                        handle_attachment(msg, uid)
            elif message.get('delivery'):
                print("[LOG-DELI] Message from #{0} delivered to #{1}.".format(str(uid)[0:4], str(uid)[0:4]))
            elif message.get('read'):
                print("[LOG-SEEN] Message from #{0} read by #{1}.".format(str(uid)[0:4], str(uid)[0:4]))

#react when the user sends some text
def handle_text(msg, uid):
    print("[LOG-MESG] User #{0} said: '{1}'.".format(str(uid)[0:4], str(msg.get('text'))))
    entity = best_match_entity(msg)
    response = bot_response(msg.get('text'), entity)
    send_message(uid, response)

#react when the user sends a sticker
def handle_sticker(msg, uid):
    print("[LOG-MESG] User #{0} sent sticker.".format(str(uid)[0:4]))
    response = recognize_sticker(str(msg.get('sticker_id')))
    send_message(uid, response)

#react when the user sends a GIFs, photos, videos, or any other non-text item:
def handle_attachment(msg, uid):
    print("[LOG-MESG] User #{0} sent gif.".format(str(uid)[0:4]))
    #Send funny gif:
    image_url = r'https://media.giphy.com/media/L7ONYIPYXyc8/giphy.gif'
    send_image(recipient_id, image_url)

def send_message(recipient_id, response):
    if type(response) == list: response = random.choice(response)
    bot.send_text_message(recipient_id, response)
    print("[LOG-RESP] Bot has answered: '" + str(response) + "'.")

def send_image(recipient_id, image_url):
    bot.send_image_url(recipient_id, image_url)
    #local file:
    #bot.send_image(recipient_id, r'C:\Users\Artur\Desktop\CODE\Chatbot Game\resources\CogitoErgoSum.jpg')
    print("[LOG-RESP] Bot has answered with a funny picture.")

def fake_typing(recipient_id, duration=3):
    bot.send_action(recipient_id, 'mark_seen')
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
