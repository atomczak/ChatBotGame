import random
from flask import Flask, request
from pymessenger.bot import Bot

#create a Flask app that will connect with fb:
app = Flask(__name__)
ACCESS_TOKEN = 'EAADioxWNLLMBAK9PGz1bkFdwbVZB7ezmap4YBt0x3MLNVdpbUwjkncpGC19er7AhJtoENCZBewGbWIPb2MxJ690OUQiWOYWKv6yLgZBPjE80vYzQuemGVxq6BkzpJZBty7ZANoNeZADJsklL3dmHkYz4NU4cU7Pk3C3zcIrSZCIswZDZD'
VERIFY_TOKEN = 'HasloOkon2018'
bot = Bot(ACCESS_TOKEN)

#We will receive messages that Facebook sends our bot at this endpoint
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        #Before allowing people to message your bot, Facebook has implemented a verify token that confirms all requests that your bot receives came from Facebook.
        token_sent = request.args.get("hub.verify_token")
        print('to był GET - wysłałem token:'+token_sent)
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                print("_________________")
                print(str(message))
                print("_________________")
                if message.get('message'):
                    #Facebook Messenger ID for user so we know where to send response back to
                    recipient_id = message['sender']['id']
                    #handle text messages:
                    if message['message'].get('text'):
                        response_sent_text = get_message(message['message'].get('text'))
                        send_message(recipient_id, response_sent_text)
                    #handle stickers:
                    if message['message'].get('text'):
                        response_sent_text = get_message(message['message'].get('text'))
                        send_message(recipient_id, response_sent_text)
                    #handle GIFs, photos, videos, or any other non-text item:
                    if message['message'].get('attachments'):
                        response_sent_nontext = get_message()
                        send_message(recipient_id, response_sent_nontext)
    return "Message Processed"

def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

#chooses a random message to send to the user
def get_message(user_message=""):
    sample_adjectives = ["random", "generic", "fake", "artificial", "arbitrary"]
    sample_noun = ["answer", "reply", "response", "message"]
    f = "."
    if user_message != "": f=" to the message: "+str(user_message)+"'."
    return random.choice(sample_adjectives)+" "+random.choice(sample_noun)+" #"+str(random.randint(1000,10000))+f

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()
