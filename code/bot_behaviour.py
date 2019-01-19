#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" This code contains functions for basic bot behaviours. """

import re
import json
import random
from code import tokens
#from code import mongodb_connection as db
from code import mysql_connection as db
from code.resources import *
from code.fb_messenger import Bot
from code import rock_paper_scissors as rps
from flask import Flask, request

#initiate the bot object:
bot = Bot(tokens.fb_access)

#fetch user ids from the DB:
users = []
for user in db.get_all('facebook_id'):
    users.append(user)

def verify_fb_token(token_sent):
    """Take token sent by facebook and verify if it matches"""
    if token_sent == tokens.fb_verification:
        return request.args.get("hub.challenge")
        print("[LOG-VERI] Token verification succesfull.")
    else:
        print("[LOG-VERI] Failed to verify token.")
    return 'Invalid verification token'

def handle_messages(user_message):
    """ Recognize the content and respond accordingly. """
    for event in user_message['entry']:
        messaging = event['messaging']
        for message in messaging:
            userid = message['sender']['id']   #sender, thus our recipient id
            if message.get('message'):
                bot.fb_send_action(userid, 'mark_seen')
                add_new_user(userid)
                message = message['message']
                if int(userid) != int(tokens.fb_bot_id):
                    if message.get('text'):
                        handle_text(message, userid, bot)
                    elif message.get('sticker_id'):
                        handle_sticker(message, userid, bot)
                    elif message.get('attachments'):
                        handle_attachment(message, userid, bot)
            elif message.get('delivery'):
                print("[LOG-DELI] Message from #{0} delivered to #{1}.".format(str(userid)[0:4], str(message['recipient']['id'])[0:4]))
            elif message.get('read'):
                print("[LOG-SEEN] Message from #{0} read by #{1}.".format(str(userid)[0:4], str(message['recipient']['id'])[0:4]))

def add_new_user(user_id):
    """ Check if already exists. If not - add to database. """
    if user_id not in users:
        #TODO withdraw more info: bot.fb_get_user_info(bot,userid)  #first_name
        db.create_player(user_id)
        users.append(user_id)
    else:
        #TODO withdraw more info from the database.
        # db.query(user_id, (first_name,))
        pass

def handle_text(message, userid, bot):
    """ React when the user sends any text. """
    text = message.get('text')
    entity = best_match_entity(message)
    user_message = message.get('text')
    if entity == "" or entity is None:
        entity = regex_pattern_matcher(user_message)   #no entity from NLP so try to find with regex
    print("[LOG-MESG] User #{0} said: '{1}' and I recognize it as: {2}.".format(str(userid)[0:4], str(message.get('text')), entity))
    if entity == "rock-paper-scissors":
        rps.play(user_message, userid, bot)     #TODO not working
        print("[LOG-ERROR-001]")
    elif entity == 'test_list_message':
        bot.fb_send_list_message(userid, ['a', 'b'], ['a', 'b'])        #TODO not working
        print("[LOG-ERROR-002]")
    elif entity == 'test_button_message':
        bot.fb_send_button_message(userid, "test", ['a', 'b'])      #TODO not working
        print("[LOG-ERROR-003]")
    elif entity == 'test_generic_message':
        bot.fb_send_generic_message(userid, ['a', 'b'])     #TODO not working
        print("[LOG-ERROR-004]")
    else:
        response = responder(entity, user_message, userid, bot)   #prepare the response based on the entity given
        if type(response) == list:
            response = random.choice(response)
        bot.fb_send_text_message(userid, response)
        db.add_conversation(userid, 'User', text)
        db.add_conversation(userid,'Bot', response)
        print("[LOG-RESP] Bot has answered: '" + str(message) + "'.")

def handle_sticker(message, userid, bot):
    """ React when the user sends a sticker. """
    bot.fb_fake_typing(userid, 0.5)
    response = recognize_sticker(str(message.get('sticker_id')))
    bot.fb_send_text_message(userid, response)
    db.add_conversation(userid,'User', '<sticker_'+str(message.get('sticker_id'))+'>')
    db.add_conversation(userid,'Bot', response)
    print("[LOG-MESG] User #{0} sent a sticker.".format(str(userid)[0:4]))
    print('[LOG-MESG] Bot answered to user #{0}: "{1}"'.format(str(userid)[0:4], str(response)))

def handle_attachment(message, userid, bot):
    """ React when the user sends a GIF, photos, videos, or any other non-text item."""
    bot.fb_fake_typing(userid, 0.8)
    image_url = r'https://media.giphy.com/media/L7ONYIPYXyc8/giphy.gif'
    bot.fb_send_image_url(userid, image_url)
    #or from local file: #bot.fb_send_image(userid, r'..\resources\CogitoErgoSum.jpg')
    db.add_conversation(userid,'User','<GIF>')
    db.add_conversation(userid, 'Bot', "<picture>")
    print("[LOG-MESG] User #{0} sent a GIF.".format(str(userid)[0:4]))
    print("[LOG-RESP] Bot has answered with a picture.")

def regex_pattern_matcher(str, pattern_dic=pattern_dictionary):
    """Regular Expression pattern finder that searches for intents from patternDictionary."""
    intent = False
    search_object = False
    for key, value in pattern_dic.items():
        if type(value) == list:
            for v in value:
                s = re.search(v, str, re.M|re.I|re.U)    #|re.U
                if s: search_object = s
        else:
            search_object = re.search(value, str, re.M|re.I|re.U)    #|re.U
        if search_object: intent = key   #cause found searchObj.group()
    return intent

def best_match_entity(message, minimum=0.9):
    """ Return best matching entity from NLP or None. """
    try:
        entities = list(message.get('nlp').get('entities').keys())
        #entities.remove("sentiment")
        confidence = []
        for c in list(message.get('nlp').get('entities').values()):
            confidence.append(c[0]['confidence'])
        print("[LOG-TEMP] max confidence: "+str(max(confidence)))
        if max(confidence)>minimum:
            # create dictionary entity:confidence:
            iterable = zip(entities, confidence)
            pairs = {key: value for (key, value) in iterable}
            best_match = max(pairs, key=pairs.get)
            print("[LOG-ENTY] Recognized entities: {0}, best is: '{1}'.".format(str(pairs), best_match))
            return best_match
        else:
            return None
    except:
        return None

def stack_items(id, item, stack_size = 3):
    """A function that lets you keep multiple (amount equal to stack_size) items in a list. The lists are
    than put in a one common dictionary. id -> dictionary index; item -> item to put in the stack"""
    global stacked_items # variable init in a a function to allow for easy function copy-pasting.
    try:
        stacked_items.get('') # checks if the variable is already created
    except:
        stacked_items = {} # if it's not, create the variable
    if id in stacked_items:
        stacked_items[id].append(item)
        if len (stacked_items[id]) > stack_size:
            stacked_items[id].pop(0)
    else:
        stacked_items[id] = []
        stacked_items[id].append(item)
