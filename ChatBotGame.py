#Python libraries that we need to import for our bot
import random
from flask import Flask, request
from pymessenger.bot import Bot
from helpers import *
import json

app = Flask(__name__)
#Tokens below should match the ones staeted on Facebook Messenger Developers website:
ACCESS_TOKEN = 'EAADioxWNLLMBAK9PGz1bkFdwbVZB7ezmap4YBt0x3MLNVdpbUwjkncpGC19er7AhJtoENCZBewGbWIPb2MxJ690OUQiWOYWKv6yLgZBPjE80vYzQuemGVxq6BkzpJZBty7ZANoNeZADJsklL3dmHkYz4NU4cU7Pk3C3zcIrSZCIswZDZD'
VERIFY_TOKEN = 'HasloOkon2018'
bot = Bot(ACCESS_TOKEN)
bot_id = 302799017185129 #spisane dla 'Test GameBot #2'
artur_id = 2321541911195477
#We will receive messages that Facebook sends our bot at this endpoint:
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        #Before interacting with bot, Facebook must verify the token:
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    else:   #if the request was not GET, it must be POST and we can just proceed with sending a message back to user
        userMessage = request.get_json()    #get user's message
        for event in userMessage['entry']:
            messaging = event['messaging']
            for message in messaging:
                #print(json.dumps(message, sort_keys=True, indent=4))
                if message.get('message'):
                    #Facebook Messenger ID for user so we know where to send response back to
                    recipient_id = message['sender']['id']
                    print("--LOG-->  THE USER {0} SAID TO {1}: '{2}'.".format(str(recipient_id)[0:4]+"...", str(message['recipient']['id'])[0:4]+"...", str(message['message'].get('text'))))
                    if int(recipient_id) != int(bot_id):
                        #handle text messages:
                        if message['message'].get('text'):
                            entity = bestMatchEntity(message)
                            response_text = botResponse(message['message'].get('text'), entity)
                            sendMessage(recipient_id, response_text)
                        #handle stickers:
                        elif message['message'].get('sticker_id'):
                            response = recognizeSticker(str(message['message'].get('sticker_id')))
                            sendMessage(recipient_id, response)
                            #sendMessage(recipient_id, str(message['message'].get('sticker_id')))
                        #handle GIFs, photos, videos, or any other non-text item:
                        elif message['message'].get('attachments'):
                            sendMessage(recipient_id, "Cool gif.")
                            image_url = r'https://vignette.wikia.nocookie.net/animal-jam-clans-1/images/8/81/Sloth-meme-lifeisabeautifulthingtoabuse.jpg/revision/latest?cb=20160627041750'
                            sendImageUrl(recipient_id, image_url)
                elif message.get('delivery'):
                    print("--LOG-->  THE MESSAGE FROM THE USER #{0} HAS BEEN DELIVERED TO THE USER #{1}.".format(str(message['sender']['id'])[0:4]+"...", str(message['recipient']['id'])[0:4]+"..."))
                elif message.get('read'):
                    print("--LOG-->  THE USER #{0} HAS READ THE MESSAGE FROM TO THE USER #{1}.".format(str(message['recipient']['id'])[0:4]+"...", str(message['sender']['id'])[0:4]+"..."))


    return "Message Processed"

#uses PyMessenger to send response to user:
def sendMessage(recipient_id, response):
    if type(response) == list: response = random.choice(response)
    bot.send_text_message(recipient_id, response)
    #print("BOT ANSWERED WITH: '" + str(response) + "'.")
    return "success"

#uses PyMessenger to send response to user:
def sendImageUrl(recipient_id, image_url):
    bot.send_image_url(recipient_id, image_url)
    #print("BOT ANSWERED WITH A COOL IMAGE.")
    #bot.send_image(recipient_id, r'C:\Users\Artur\Desktop\CODE\Chatbot Game\resources\CogitoErgoSum.jpg')
    return "success"

#If the program (ChatBotGame.py) is executed (double-clicked), it will set name to main, thus run app:
if __name__ == "__main__":
    app.run()
