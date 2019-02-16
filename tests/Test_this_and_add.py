"""
#from wit import Wit
                response = client.message(msg=text, context={'session_id':fb_id})
                handle_message(response=response, fb_id=fb_id)

def first_entity_value(entities, entity):
    """
    #Returns first entity value
    """
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val

def handle_message(response, fb_id):
    """
    #Customizes our response to the message and sends it
    """
    entities = response['entities']
    # Checks if user's message is a greeting
    # Otherwise we will just repeat what they sent us
    greetings = first_entity_value(entities, 'greetings')
    if greetings:
        text = "hello!"
    else:
        text = "We've received your message: " + response['_text']
    # send message
    fb_message(fb_id, text)


# Setup Wit Client
client = Wit(access_token=WIT_TOKEN)
"""
