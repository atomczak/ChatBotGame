#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" This code contains functions for basic bot behaviours. """

import re
import json
import random
from Responder_app import local_tokens, database, witai
if local_tokens: from code import tokens_local as tokens
else: from code import tokens
if database: from code import mysql_connection as db
from code.respond import *
from code.fb_messenger import Bot
from code import rock_paper_scissors as rps
from flask import Flask, request
import pprint
import logging
import os
log = logging.getLogger(os.path.basename(__file__))

#initiate the bot object:
bot = Bot(tokens.fb_access)

#fetch user ids from the DB:
users = []
if database:
    for user in db.get_all('facebook_id'):
        users.append(user)

def handle_messages(user_message):
    """ Recognize the content and respond accordingly. """
    for entry in user_message['entry']:
        message_id = entry['id']
        messaging = entry['messaging']
        for message in messaging:
            userid = message['sender']['id']   #sender, thus our recipient id
            if message.get('delivery'):
                deli = message['delivery']
                #mid = deli.get('mid')
                mid = "abcdefghijklmn"
                if int(message['recipient']['id']) == int(tokens.fb_bot_id):
                    log.info("Message {0} from {1} delivered".format(str(mid)[0:6], str(userid[0:5])))
                else:
                    log.info("Message {0} delivered to {1}".format(str(mid)[0:6], str(message['recipient']['id'][0:5])))
            elif message.get('read'):
                if int(message['recipient']['id']) == int(tokens.fb_bot_id):
                    log.info("Message from {0} read by bot".format(str(userid[0:5])))
                else:
                    log.info("Message from bot read by {1}".format(message['recipient']['id'][0:5]))
            elif message.get('message'):
                bot.fb_send_action(userid, 'mark_seen')
                add_new_user(userid)
                message = message['message']
                user_message = message.get('text')
                mid = message.get('mid')
                if int(userid) != int(tokens.fb_bot_id):
                    if message.get('text'):
                        log.info("Message {0} from {1}:\n{2}USER: {3}".format(str(mid)[0:6], str(userid)[0:5], 20*" ", user_message))
                        handle_text(message, userid, bot)
                    elif message.get('sticker_id'):
                        log.info("Message {0} from {1}:\n{2}USER: <sticker id={3}>".format(str(mid)[0:6], str(userid)[0:5], 20*" ", str(message.get('sticker_id')) ))
                        handle_sticker(message, userid, bot)
                    elif message.get('attachments'):
                        log.info("Message {0} from {1}:\n{2}USER: <GIF link={3}>".format(str(mid)[0:6], str(userid)[0:5], 20*" ", str(message.get('url')) ))
                        handle_attachment(message, userid, bot)
                else:
                    if message.get('text'):
                        log.info("Bot's message {0} to {1}:\n{2}BOT:  {3}".format(str(mid)[0:6], str(userid)[0:5], 20*" ", user_message))
                    elif message.get('sticker_id'):
                        log.info("Bot's message {0} to {1}:\n{2}BOT:  <sticker id={3}>".format(str(mid)[0:6], str(userid)[0:5], 20*" ", str(message.get('sticker_id')) ))
                    elif message.get('attachments'):
                        log.info("Bot's message {0} to {1}:\n{2}BOT:  <GIF link={3}>".format(str(mid)[0:6], str(userid)[0:5], 20*" ", str(message.get('url')) ))
            else:
                log.error("Unknown message type! Content: " + message)

def add_new_user(user_id):
    """ Check if already exists. If not - add to database. """
    if user_id not in users:
        #TODO withdraw more info: bot.fb_get_user_info(bot,userid)  #first_name
        if database: db.create_player(user_id)
        users.append(user_id)
    else:
        #TODO withdraw more info from the database.
        #if database: db.query(user_id, (first_name,))
        pass

def handle_text(message, userid, bot):
    """ React when the user sends any text. """
    entity = best_entity(message)
    user_message = message.get('text')
    mid = message.get('mid')
    if entity == "" or entity is None:
        entity = regex_pattern_matcher(user_message)   #no entity from NLP so try to find with regex
        log.info("Message {0} from {1} recognized as {2} using REGEX".format(str(mid)[0:6], str(userid)[0:5], entity))
    else:
        log.info("Message {0} from {1} recognized as {2}={3} using NLP from FB".format(str(mid)[0:6], str(userid)[0:5], entity[0], str(entity[1])[0:5]))
        entity = entity[0]
    # React:
    response = responder(entity, user_message, userid, bot)   #prepare the response based on the entity given
    if response != "already sent":
        if type(response) == list:
            response = random.choice(response)
        bot.fb_send_text_message(userid, response)
        if database: db.add_conversation(userid, 'User', user_message)
        if database: db.add_conversation(userid, 'Bot', response)

def handle_sticker(message, userid, bot):
    """ React when the user sends a sticker. """
    bot.fb_fake_typing(userid, 0.5)
    sticker_id = str(message.get('sticker_id'))
    sticker_name = recognize_sticker(sticker_id)
    response = sticker_response(sticker_name)
    bot.fb_send_text_message(userid, response)
    mid = "abcdefghijklmn"
    if database: db.add_conversation(userid,'User', '<sticker_{0}_{1}>'.format(sticker_name, str(sticker_id)))
    if database: db.add_conversation(userid,'Bot', response)
    log.info("Message {0} from {1} recognized as '{1}' sticker (id={2})".format(str(mid)[0:6], str(userid)[0:5], sticker_name, str(sticker_id)))
    log.info("Bot answer to {1}: '{0}'".format(response, str(userid)))

def handle_attachment(message, userid, bot):
    """ React when the user sends a GIF, photos, videos, or any other non-text item."""
    bot.fb_fake_typing(userid, 0.8)
    image_url = r'https://media.giphy.com/media/L7ONYIPYXyc8/giphy.gif'
    bot.fb_send_image_url(userid, image_url)
    #or from local file: #bot.fb_send_image(userid, r'..\resources\CogitoErgoSum.jpg')
    if database: db.add_conversation(userid,'User','<GIF>')
    if database: db.add_conversation(userid, 'Bot', "<GIF>")
    log.info("Bot: '{0}' [To: #{1}]".format('<GIF>', str(userid)))

def regex_pattern_matcher(str, pat_dic=pattern_dictionary):
    """Regular Expression pattern finder that searches for intents from patternDictionary."""
    intent = False
    search_object = False
    for key, value in pat_dic.items():
        if type(value) == list:
            for v in value:
                s = re.search(v, str, re.M|re.I|re.U)    #|re.U
                if s: search_object = s
        else:
            search_object = re.search(value, str, re.M|re.I|re.U)    #|re.U
        if search_object: intent = key   #cause found searchObj.group()
    return intent

def best_entity(message, minimum=0.85):
    """ Return best matching entity from NLP or None. """
    try:
        entities = list(message.get('nlp').get('entities').keys())
        #entities.remove("sentiment")
        confidence = []
        for c in list(message.get('nlp').get('entities').values()):
            confidence.append(c[0]['confidence'])
        if max(confidence)>minimum:
            # create dictionary entity:confidence:
            iterable = zip(entities, confidence)
            pairs = {key: value for (key, value) in iterable}
            best_match = max(pairs, key=pairs.get)
            return [best_match, str(max(confidence))]
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
