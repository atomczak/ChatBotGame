import random

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
    }.get(intent, ["No idea what you mean by that.","huh?","I don't get it","pardon me?"])

def recognize_sticker(sticker_id):
    if sticker_id.startswith('369239263222822'):  response = "I take that blue thumb as yes."   #thumb
    elif sticker_id.startswith('369239343222814'):  response = "ho, what a big thumb!"    #thumb+
    elif sticker_id.startswith('369239383222810'): response = "That is a big thumb."   #thumb++
    elif sticker_id.startswith('523675'):  response = "Cute dog :)"    #dog
    elif sticker_id.startswith('631487'):  response = "Does this cactus have a second meaning? :)"    #cactus
    elif sticker_id.startswith('788676574539860'):  response = "I know it's great, that's what I do!"    #dogo Great Work
    elif sticker_id.startswith('78817'):  response = "Cute fluffy dog! <3"    #dogo
    elif sticker_id.startswith('7926'):  response = "Cute fluffy dog!"    #dogo
    elif sticker_id.startswith('1845'):  response = "I don't like birds, including doves"    #dove
    elif sticker_id.startswith('1846'):  response = "I don't like birds, including doves"    #dove
    elif sticker_id.startswith('14488'):  response = "Miauuuu :)"    #kitten
    elif sticker_id.startswith('65444'):  response = "🙈 🙉 🙊"    #monkey
    elif sticker_id.startswith('12636'):  response = "Thats a big emoji"    #big emoji
    elif sticker_id.startswith('1618'):  response = "It reminds me of my turtle... R.I.P"    #turtle
    elif sticker_id.startswith('8509'):  response = "hehe, office stickers from the 90s are so old-school"    #office
    elif sticker_id.startswith('2556'):  response = "koko?"    #chicken
    elif sticker_id.startswith('2095'):  response = "what does the fox say?!"    #fox
    elif sticker_id.startswith('56663'):  response = "Kung fury! 👊👊👊"    #Kung fury
    elif sticker_id.startswith('30261'):  response = "cute sloth"    #sloth
    else:   response = "Cool sticker."
    return response
