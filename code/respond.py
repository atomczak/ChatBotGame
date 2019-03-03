import random
from code import rock_paper_scissors as rps
from code.fb_messenger import Bot
from Responder_app import local_tokens, database, witai
if local_tokens: from code import tokens_local as tokens
else: from code import tokens
import logging
import os
log = logging.getLogger(os.path.basename(__file__))
if database: from code import mysql_connection as db
from time import sleep

#Set of intents and patterns to recognize them:
pattern_dictionary = {
        'greetings': [r'\b(hi|h[ea]+l+?o|h[ea]+[yj]+|yo+|welcome|(good)?\s?(morning?|evenin?)|hola|howdy|shalom|salam|czesc|witaj|siemk?a|marhaba|salut)\b'],
        #'greetings': [r'\b(hi|h[ea]+l+?o|h[ea]+[yj]+|yo+|welcome|(good)?\s?(morning?|evenin?)|hola|howdy|shalom|salam|czesc|witaj|siemk?a|marhaba|salut)\b', r'(\🖐|\🖖|\👋|\🤙)'],     #🖐🏻,🖖🏻,👋🏻,🤙🏻,🖐🏼,🖖🏼,👋🏼,🤙🏼,🖐🏽,🖖🏽,👋🏽,🤙🏽,🖐🏾,🖖🏾,👋🏾,🤙🏾,🖐🏿,🖖🏿,👋🏿,🤙🏿
        'yes': r'\b(yes|si|ok|kk|ok[ae]y|su+re|affirmative|confirm|good)\b',
        #'yes': [r'\b(yes|si|ok|kk|ok[ae]y|confirm)\b',r'(\✔️|\☑️|\👍|\👌)'],    #👍🏻,👌🏻,👍🏼,👌🏼,👍🏽,👌🏽,👍🏾,👌🏾,👍🏿,👌🏿
        'no': r'\b(n+o+|decline|negative|n+o+pe)\b',
        #'no': [r'\b(n+o+|decline|negative|n+o+pe)\b', r'\👎'],    #👎🏻,👎🏼,👎🏽,👎🏾,👎🏿
        'maybe' : r'\b(don\'?t\sknow?|maybe|perhaps?|not\ssure|y+)\b',
        'curse' : [r'\b(fuck|kurwa)\b', r'pierd[oa]l', r'\bass'],
        #'curse' : [r'\b(fuck|kurwa)\b', r'pierd[oa]l', r'\bass', r'\🖕'],  #🖕🏻,🖕🏼,🖕🏽,🖕🏾,🖕🏿
        'uname' : [r'y?o?ur\sname\??', r'(how|what)[\s\S]{1,15}call(ing)?\sy?o?u\??'],
        'ureal' : r'\by?o?u\s(real|true|bot|ai|human|person|man)\b',
        "secret" : r'(secret|password|key)',
        "rpsgame" : [r'start', r'play', r'game', r'rock ?paper ?scissors', r'rock', r'✊', r'paper', r'✋', r'scissors', r'✌'],
        "love" : r'love',
        #"love" : [r'love',r'(\❤️|\🧡|\💛|\💚|\💙|\💜|\🖤)'],
        'test_list_message': r'list message',
        'test_button_message': r'button message',
        'test_generic_message': r'generic message',
        'test_quick_replies': r'quick replies',
        'bye': r'(bye|exit|quit|end)'
    }

#Set of responses for particular intents:
def responder(intent, user_message="", userid="", bot=""):
    switcher = {
        "greetings":   greetings,
        "yes":         yes,
        "no":          no,
        "maybe":       maybe,
        "curse":       curse,
        "rps-game":    rpsgame,
        "uname":       uname,
        "ureal":       ureal,
        "secret":      secret,
        "love":        love,
        "thanks":      thanks,
        "datetime":    datetime,
        "money":       money,
        "phone":       phone,
        "email":       email,
        "distance":    distance,
        "quantity":    quantity,
        "temperature": temperature,
        "volume":      volume,
        "location":    location,
        "duration":    duration,
        "url":         url,
        "sentiment":   sentiment,
        "rpsgame":     rpsgame,
        "test_list_message":    test_list_message,
        "test_button_message":  test_button_message,
        "test_generic_message": test_generic_message,
        "test_quick_replies":   test_quick_replies,
        "bye":          bye
    }
    # Get the function from switcher dictionary
    func = switcher.get(intent, default_message)
    # previous version with bug: func = switcher.get(intent, lambda user_message, userid, bot : default_message)
    return func(user_message, userid, bot)

def default_message(user_message, userid="", bot=""):
    return ["Please rephrase it.",
            "Sorry, I have no idea what you mean by that.",
            "Excuse me?",
            "Sorry, I don't get it",
            "pardon me?"]

def greetings(user_message, userid="", bot=""):
    return ["{0}! How are you doing? Do you want to play Rock Paper Scissors?".format(user_message.split(' ', 1)[0].capitalize()),
            "{0}! What's up? Wanna play Rock Paper Scissors?".format(user_message.split(' ', 1)[0].capitalize())]

def yes(user_message, userid="", bot=""):
    rps.play("new game", userid, bot)
    return "already sent"

def no(user_message, userid="", bot=""):
    return [":(",
            "nooo",
            "why not?",
            "Nobody says no to me!"]

def maybe(user_message, userid="", bot=""):
    return "'{0}'? You should be sure by now.".format(user_message.capitalize())

def curse(user_message, userid="", bot=""):
    return ["{0}***? bad boy...".format(user_message[0:2], userid="", bot=""),
            "not nice",
            "Calm down!",
            "same for you :P",
            "yeah? you too"]

def rpsgame(user_message, userid="", bot=""):
    rps.play(user_message, userid, bot)
    return "already sent"

def uname(user_message, userid="", bot=""):
    return ["My name is Khan 😎",
            "chicka-chicka Slim Shady 😎",
            "👽",
            "🤖",
            "they call me the man with no name"]

def ureal(user_message, userid="", bot=""):
    return ["Cogito Ergo Sum","What is real?"]

def secret(user_message, userid="", bot=""):
    return ["😈",
            "😎",
            "💩",
            "🤠",
            "💀",
            "👽",
            "🤖",
            "🙈🙉🙊"]

def love(user_message, userid="", bot=""):
    return "I love you too {0}{1}{2}!".format(random.choice(["❤️","🧡","💛","💚","💙","💜","🖤"]),random.choice(["❤️","🧡","💛","💚","💙","💜","🖤"]),random.choice(["❤️","🧡","💛","💚","💙","💜","🖤"]))

def thanks(user_message, userid="", bot=""):
    return ["No problem",
            "My pleasure!"]

def datetime(user_message, userid="", bot=""):
    return "Let me check in my calendar..."

def money(user_message, userid="", bot=""):
    return "💰💰💰!"

def phone(user_message, userid="", bot=""):
    return "My 📞 is 123-123-123 ☎️"

def email(user_message, userid="", bot=""):
    return "I don't have any email"

def distance(user_message, userid="", bot=""):
    return "it's not that far 🚗"

def quantity(user_message, userid="", bot=""):
    return "ok, that's a lot."

def temperature(user_message, userid="", bot=""):
    return "been to colder places ⛄️"

def volume(user_message, userid="", bot=""):
    return "I can handle it."

def location(user_message, userid="", bot=""):
    return "I will check where it is on the map"

def duration(user_message, userid="", bot=""):
    return "I got plenty of time ⌚️"

def url(user_message, userid="", bot=""):
    return ["you mind if I don't open that?",
            "cool link, what's that?",
            "you want me to open it"]

def sentiment(user_message, userid="", bot=""):
    return ["ehhh...",
            "good old times."]

def test_list_message(user_message, userid="", bot=""):
    if database: db.add_conversation(userid, 'User', user_message)
    if database: db.add_conversation(userid, 'Bot', '<sent list message>')
    bot.fb_send_list_message(userid, ['test_value_1', 'test_value_2'], ['test_value_3', 'test_value_4']) #TODO not working
    return "already sent"

def test_button_message(user_message, userid="", bot=""):
    if database: db.add_conversation(userid, 'User', user_message)
    if database: db.add_conversation(userid, 'Bot', '<sent button message>')
    bot.fb_send_button_message(userid, "test", ['test_value_1', 'test_value_2']) #TODO not working
    return "already sent"

def test_generic_message(user_message, userid="", bot=""):
    if database: db.add_conversation(userid, 'User', user_message)
    if database: db.add_conversation(userid, 'Bot', '<sent generic message>')
    # temp: bot.fb_send_test_message(userid, ['test_value_1', 'test_value_2'])
    bot.fb_send_generic_message(userid, ['Test_value_1', 'Test_value_2'])
    # bot.fb_send_generic_message(userid, [['Title1','Subtitle1','image_url1',buttons=['title1','url1']],['Title2','Subtitle2','image_url2',buttons=['title2','url2']]])
    return "already sent"

def test_quick_replies(user_message, userid="", bot=""):
    if database: db.add_conversation(userid, 'User', user_message)
    if database: db.add_conversation(userid, 'Bot', '<sent quick replies message>')
    bot.fb_send_quick_replies(userid, "This is a test of quick replies", ['test_value_1', 'test_value_2', 'test_value_3']) #TODO test if working
    return "already sent"

def bye(user_message, userid="", bot=""):
    return "You going already? Goodbye then!"

def recognize_sticker(sticker_id):
    if sticker_id.startswith('369239263222822'):  sticker_name = 'thumb'
    elif sticker_id.startswith('369239343222814'):  sticker_name = 'thumb+'
    elif sticker_id.startswith('369239383222810'): sticker_name = 'thumb++'
    elif sticker_id.startswith('523675'):  sticker_name = 'dogo'
    elif sticker_id.startswith('631487'):  sticker_name = 'cactus'
    elif sticker_id.startswith('788676574539860'):  sticker_name = 'dogo_great'
    elif sticker_id.startswith('78817'):  sticker_name = 'dogo'
    elif sticker_id.startswith('7926'):  sticker_name = 'dogo'
    elif sticker_id.startswith('1845'):  sticker_name = 'bird'
    elif sticker_id.startswith('1846'):  sticker_name = 'bird'
    elif sticker_id.startswith('14488'):  sticker_name = 'cat'
    elif sticker_id.startswith('65444'):  sticker_name = 'monkey'
    elif sticker_id.startswith('12636'):  sticker_name = 'emoji'
    elif sticker_id.startswith('1618'):  sticker_name = 'turtle'
    elif sticker_id.startswith('8509'):  sticker_name = 'office'
    elif sticker_id.startswith('2556'):  sticker_name = 'chicken'
    elif sticker_id.startswith('2095'):  sticker_name = 'fox'
    elif sticker_id.startswith('56663'):  sticker_name = 'kungfurry'
    elif sticker_id.startswith('30261'):  sticker_name = 'sloth'
    else:  sticker_name = 'unknown'
    return sticker_name

def sticker_response(sticker_name, userid, bot):
    if sticker_name == 'thumb' or sticker_name == 'thumb+' or sticker_name == 'thumb++':
        bot.fb_send_text_message(userid, "I take this thumb as yes")
        yes("new game", userid, bot)
        return "already sent"
    else:
        return [{
            'cactus' : "Does this cactus have a second meaning? :)",
            'dogo' : "Cute dog :)",
            'dogo_great' : "I know it's great, that's what I do!",
            'bird' : "I don't like birds, including doves",
            'cat' : "Miauuuu :)",
            'monkey' : "🙈 🙉 🙊",
            'emoji' : "Thats a big emoji",
            'turtle' : "It reminds me of my turtle... R.I.P",
            'office' : "hehe, office stickers from the 90s are so old-school",
            'chicken' : "koko?",
            'fox' : "what does the fox say?!",
            'kungfurry' : "Kung fury! 👊👊👊",
            'sloth' : "cute sloth"
         }.get(sticker_name, ["Cool sticker.", "I don't know how to relate to that sticker"]), sticker_name]
