import random
from code import rock_paper_scissors as rps

#Set of intents and patterns to recognize them:
pattern_dictionary = {
        'greetings': [r'\b(hi|h[ea]+l+?o|h[ea]+[yj]+|yo+|welcome|(good)?\s?(morning?|evenin?)|hola|howdy|shalom|salam|czesc|witaj|siemk?a|marhaba|salut)\b'],
        #'greetings': [r'\b(hi|h[ea]+l+?o|h[ea]+[yj]+|yo+|welcome|(good)?\s?(morning?|evenin?)|hola|howdy|shalom|salam|czesc|witaj|siemk?a|marhaba|salut)\b', r'(\🖐|\🖖|\👋|\🤙)'],     #🖐🏻,🖖🏻,👋🏻,🤙🏻,🖐🏼,🖖🏼,👋🏼,🤙🏼,🖐🏽,🖖🏽,👋🏽,🤙🏽,🖐🏾,🖖🏾,👋🏾,🤙🏾,🖐🏿,🖖🏿,👋🏿,🤙🏿
        'yes': r'\b(yes|si|ok|kk|ok[ae]y|confirm|good)\b',
        #'yes': [r'\b(yes|si|ok|kk|ok[ae]y|confirm)\b',r'(\✔️|\☑️|\👍|\👌)'],    #👍🏻,👌🏻,👍🏼,👌🏼,👍🏽,👌🏽,👍🏾,👌🏾,👍🏿,👌🏿
        'no': r'\b(n+o+|decline|negative|n+o+pe)\b',
        #'no': [r'\b(n+o+|decline|negative|n+o+pe)\b', r'\👎'],    #👎🏻,👎🏼,👎🏽,👎🏾,👎🏿
        'maybe' : r'\b(don\'?t\sknow?|maybe|perhaps?|not\ssure|y+)\b',
        'curse' : [r'\b(fuck|kurwa)\b', r'pierd[oa]l', r'\bass'],
        #'curse' : [r'\b(fuck|kurwa)\b', r'pierd[oa]l', r'\bass', r'\🖕'],  #🖕🏻,🖕🏼,🖕🏽,🖕🏾,🖕🏿
        'uname' : [r'y?o?ur\sname\??', r'(how|what)[\s\S]{1,15}call(ing)?\sy?o?u\??'],
        'ureal' : r'\by?o?u\s(real|true|bot|ai|human|person|man)\b',
        "secret" : r'(secret|password|key)',
        "rps-game" : [r'start', r'play', r'game', r'rock ?paper ?scissors', r'rock', r'✊', r'paper', r'✋', r'scissors', r'✌'],
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
    return {
        "greetings": "{0}! How are you doing?".format(user_message.split(' ', 1)[0].capitalize()),
        "yes": ["You confirm, good","great","perfect","good","(y)"],
        "no": [":(","nooo","why not?","Nobody says no to me!"],
        "maybe" : "'{0}'? You should be sure by now.".format(user_message.capitalize()),
        "curse" : ["you {0}".format(user_message),"not nice","Calm down!","same for you","yeah? you too"],
        "rps-game" : "",
        "uname" : ["My name is Khan 😎","chicka-chicka Slim Shady 😎","👽","🤖","they call me the man with no name"],
        "ureal" : ["Cogito Ergo Sum","What is real?"],
        "secret" : ["😈","😎","💩","🤠","💀","👽","🤖","🙈🙉🙊"],
        "love" : "I love you too {0}{1}{2}!".format(random.choice(["❤️","🧡","💛","💚","💙","💜","🖤"]),random.choice(["❤️","🧡","💛","💚","💙","💜","🖤"]),random.choice(["❤️","🧡","💛","💚","💙","💜","🖤"])),
        "thanks" : ["No problem","My pleasure!"],
        "datetime" : "Let me check in my calendar...",
        "amount_of_money" : "💰💰💰!",
        "phone_number" : "My 📞 is 123-123-123 ☎️",
        "email" : "Email, how oldschool is that.",
        "distance" : "it's not that far 🚗",
        "quantity" : "ok, that's a lot.",
        "temperature" : "brrrr ⛄️",
        "volume" : "I can handle it.",
        "location" : "I will check where it is on the map",
        "duration" : "I got plenty of time ⌚️",
        "url" : ["you mind if I don't open that?","cool link, what's that?","you want me to open it"],
        "sentiment" : ["ehhh...","good old times."],
        "rps-game" : rps.play(user_message, userid, bot),
        'test_list_message' : bot.fb_send_list_message(userid, ['a', 'b'], ['a', 'b']), #TODO not working
        'test_button_message' : bot.fb_send_button_message(userid, "test", ['a', 'b']), #TODO not working
        'test_generic_message' : bot.fb_send_generic_message(userid, ['a', 'b']), #TODO not working
        'test_quick_replies': bot.fb_send_quick_replies(userid, "This is a test of quick replies", ['a', 'b', 'c']), #TODO test if working
        "bye" : "You going already? Goodbye then!"
    }.get(intent, ["No idea what you mean by that.","huh?","I don't get it","pardon me?"])

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

def sticker_response(sticker_name):
    return [{
        'thumb' : "I take that blue thumb as yes.",
        'thumb+' : "ho, what a big thumb!",
        'thumb++' : "That is a big thumb.",
        'cactus' : "Does this cactus have a second meaning? :)",
        'dogo' : "Cute dog :)",
        'dogo_great' : "I know it's great, that's what I do!",
        'bird' : "I don't like birds, including doves",
        'cat : '"Miauuuu :)",
        'monkey' : "🙈 🙉 🙊",
        'emoji' : "Thats a big emoji",
        'turtle' : "It reminds me of my turtle... R.I.P",
        'office' : "hehe, office stickers from the 90s are so old-school",
        'chicken' : "koko?",
        'fox' : "what does the fox say?!",
        'kungfurry' : "Kung fury! 👊👊👊",
        'sloth' : "cute sloth"
     }.get(sticker_name, ["Cool sticker.", "I don't know how to relate to that sticker"]), sticker_name]
