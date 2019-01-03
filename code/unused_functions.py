from datetime import date
from time import sleep
from difflib import get_close_matches

def time(message):
    timestamp = float(message['timestamp'])/1000
    return date.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

#Lookup the definition of the word in the dictionary:
def translate(word):
    encyclopedia = json.load(open("../resources/Encyclopedia.json"))    #TODO moze lepiej zeby takie rzeczy się otwierało raz - przy starcie apki?
    word = word.lower()
    if word in encyclopedia:
        return encyclopedia[word]
    elif len(get_close_matches(word, encyclopedia.keys())) > 0:
        return ["CloseMatch", encyclopedia[get_close_matches(word, encyclopedia.keys())[0]], encyclopedia[get_close_matches(w, encyclopedia.keys())[1]]]
