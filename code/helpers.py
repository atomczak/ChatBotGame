﻿import re
import random
from pymessenger.bot import Bot
import json
from difflib import get_close_matches

#Prepare an answer, based on the user message:
def botResponse(userAns, entity=""):
    if entity == "" or entity is None:
        entity = regExPatternMatcher(userAns)   #no entity from NLP so try to find with regex
    if entity == "koko":
        #encyclopedia
        pass
    response = responder(entity, userAns)   #prepare the response based on the entity given
    if type(response) == list:
        response = random.choice(response)
    #if response[0:5] == "PIC:": #TODO
    #elif response[0:5] == "GIF:": #TODO
    return response

#Regular Expression pattern finder that searches for intents from patternDictionary:
def regExPatternMatcher(str):
    intent = False
    searchObj = False
    for key, value in patternDictionary.items():
        if type(value) == list:
            for v in value:
                s = re.search(v, str, re.M|re.I|re.U)    #|re.U
                if s: searchObj = s
        else:
            searchObj = re.search(value, str, re.M|re.I|re.U)    #|re.U
        if searchObj: intent = key   #cause found searchObj.group()
    return intent

#Set of intents and patterns to recognize them:
patternDictionary = {
        'greetings': [r'\b(hi|h[ea]+l+?o|h[ea]+[yj]+|yo+|welcome|(good)?\s?(morning?|evenin?)|hola|howdy|shalom|salam|czesc|witaj|siemk?a|marhaba|salut)\b'],
        #'greetings': [r'\b(hi|h[ea]+l+?o|h[ea]+[yj]+|yo+|welcome|(good)?\s?(morning?|evenin?)|hola|howdy|shalom|salam|czesc|witaj|siemk?a|marhaba|salut)\b', r'(\🖐|\🖖|\👋|\🤙)'],     #🖐🏻,🖖🏻,👋🏻,🤙🏻,🖐🏼,🖖🏼,👋🏼,🤙🏼,🖐🏽,🖖🏽,👋🏽,🤙🏽,🖐🏾,🖖🏾,👋🏾,🤙🏾,🖐🏿,🖖🏿,👋🏿,🤙🏿
        'yes': r'\b(yes|si|ok|kk|ok[ae]y|confirm|good)\b',
        #'yes': [r'\b(yes|si|ok|kk|ok[ae]y|confirm)\b',r'(\✔️|\☑️|\👍|\👌)'],    #👍🏻,👌🏻,👍🏼,👌🏼,👍🏽,👌🏽,👍🏾,👌🏾,👍🏿,👌🏿
        'no': r'\b(n+o+|decline|negative|n+o+pe)\b',
        #'no': [r'\b(n+o+|decline|negative|n+o+pe)\b', r'\👎'],    #👎🏻,👎🏼,👎🏽,👎🏾,👎🏿
        'maybe' : r'\b(don\'?t\sknow?|maybe|perhaps?|not\ssure|y+)\b',
        'curse' : [r'\b(fuck|kurwa)\b', r'pierd[oa]l', r'\bass'],
        #'curse' : [r'\b(fuck|kurwa)\b', r'pierd[oa]l', r'\bass', r'\🖕'],  #🖕🏻,🖕🏼,🖕🏽,🖕🏾,🖕🏿
        'uname?' : [r'y?o?ur\sname\??', r'(how|what)[\s\S]{1,15}call(ing)?\sy?o?u\??'],
        'ureal?' : r'\by?o?u\s(real|true|bot|ai|human|person|man)\b',
        "secret" : r'(secret|password|key)',
        "love" : r'love',
        #"love" : [r'love',r'(\❤️|\🧡|\💛|\💚|\💙|\💜|\🖤)'],
        'bye': r'(bye|exit|quit|end)'
    }

#Set of responses for particular intents:
def responder(intent, userAns=""):
    return {
        "greetings": "{0}! How are you doing?".format(userAns.split(' ', 1)[0].capitalize()),
        "yes": ["You confirm, good","great","perfect","good","(y)"],
        "no": [":(","nooo","why not?","Nobody says no to me!"],
        "maybe" : "'{0}'? You should be sure by now.".format(userAns.capitalize()),
        "curse" : ["you {0}".format(userAns),"not nice","Calm down!","same for you","yeah? you too"],
        "uname?" : ["My name is Khan 😎","chicka-chicka Slim Shady 😎","👽","🤖","they call me the man with no name"],
        "ureal?" : ["Cogito Ergo Sum","What is real?"],
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
        "bye": "You going already? Goodbye then!"
    }.get(intent, ["No idea what you mean by that.","huh?","I don't get it","pardon me?"])    # is default if entity not found

def recognizeSticker(sticker_id):
    if sticker_id.startswith('369239263222822'):  response = "I take that blue thumb as yes."   #thumb
    elif sticker_id.startswith('369239343222814'):  response = "ho, what a big thumb!"    #thumb+
    elif sticker_id.startswith('369239383222810'): response = "That is a big thumb."   #thumb++
    elif sticker_id.startswith('523675'):  response = "Cute dog :)"    #dog
    elif sticker_id.startswith('631487'):  response = "Does this cactus have a second meaning? :)"    #cactus
    elif sticker_id.startswith('78817'):  response = "Cute fluffy dog! <3"    #dogo
    elif sticker_id.startswith('788676574539860'):  response = "I know it's great, that's what I do!"    #dogo Great Work
    elif sticker_id.startswith('7926'):  response = "Cute fluffy dog! <3"    #dogo
    elif sticker_id.startswith('1845'):  response = "I don't like birds, including doves"    #dove
    elif sticker_id.startswith('1846'):  response = "I don't like birds, including doves"    #dove
    elif sticker_id.startswith('14488'):  response = "Miauuuu :)"    #kitten
    elif sticker_id.startswith('65444'):  response = "🙈 🙉 🙊"    #monkey
    elif sticker_id.startswith('12636'):  response = "I hate those big emojis!"    #big emoji
    elif sticker_id.startswith('1618'):  response = "It reminds me of my turtle... R.I.P"    #turtle
    elif sticker_id.startswith('8509'):  response = "hehe, office stickers from the 90s are so old-school"    #office
    elif sticker_id.startswith('2556'):  response = "bro-ko-ko-ko!"    #chicken
    elif sticker_id.startswith('2095'):  response = "what does the fox say?!"    #fox
    elif sticker_id.startswith('56663'):  response = "Kung fury! 👊👊👊"    #Kung fury
    elif sticker_id.startswith('30261'):  response = "sloth"    #sloth
    else:   response = "Cool sticker."
    return response

def bestMatchEntity(message):
    try:
        entities = list(message['message'].get('nlp').get('entities').keys())
        #entities.remove("sentiment")
        confidence = []
        for c in list(message['message'].get('nlp').get('entities').values()):
            confidence.append(c[0]['confidence'])
        # create dictionary entity:confidence:
        iterable = zip(entities,confidence)
        pairs = {key: value for (key, value) in iterable}
        bestMatch = max(pairs, key=pairs.get)
        print("--LOG-->-->  RECOGNIZED ENTITIES: {0}, from which the best match is: '{1}'.".format(str(pairs), bestMatch))
        return bestMatch
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

#Lookup the definition of the word in the dictionary:
def guessSong(userAns):
    lyrics = json.load(open("../rest/billboard-data/years/1984.json"))   #TODO moze lepiej zeby takie rzeczy się otwierało raz - przy starcie apki?
    userAns = userAns.lower()
    for song in lyrics:
        if userAns in song['lyrics']:
            print("Oh, you mean that {0} song by {1}? I think '{2}' was the name".format(song['year'],song['artist'],song['title']))
            print("'"+song['lyrics'].split("\n")[0])
            print(song['lyrics'].split("\n")[1])
            print(song['lyrics'].split("\n")[1]+"'")

    #elif len(get_close_matches(userAns, lyrics)) > 0:
    #    return ["CloseMatch", lyrics[get_close_matches(userAns, lyrics)[0]], lyrics[get_close_matches(userAns, lyrics)[1]]]

"""
#Answer with the definition of the word from the dictionary:
output = translate(word)
if output[0] == "CloseMatch":
    ...
elif type(output) == list:
    for item in output:
        print("BOT: " + item)
else:
    print("BOT: " + output)

if w in data:
    return data[w]
elif len(get_close_matches(w, data.keys())) > 0:
    print("BOT: Did you mean %s instead?" % get_close_matches(w, data.keys())[0])
    yn = input("YOU: ")
    if yn.lower() == "y" or yn.lower() == "yes" or yn.lower() == "":
        return data[get_close_matches(w, data.keys())[0]]
    elif yn.lower() == "n" or yn.lower() == "no":
        return "then I have no idea what it is..."
    else:
        return "pardon?"
else:
    return "I'm confused, what is it?"
"""
#take token sent by facebook and verify if it matches:
def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'
