___ProjectWiki_______________________________________

Info:
- 'code' - contains all the neccesarry methods and classes
- 'code/helpers.py' - main set of methods
- 'resources' - contains all media like json dictionaries, graphics, etc.
- 'tests' - set of tests written for particular parts of the app
- 'Responder_app.py' - the Flask app itselfs - all logic is in external modules
- '__init__' - to treat repo as a library https://stackoverflow.com/questions/448271/what-is-init-py-for
- TODO - tasks to be done can be found in Github/Projects/Todo

___mongodb_connection.py_________________________

mongodb_connection.py sample functions:

- adding a male user with the facebook_id = 'Test', first_name = 'Abc', last_name = 'Efg':  
    create_player(facebook_id='Test', first_name='Abc', last_name='Efg', sex='Male')    
    
- updating the last name of the player with facebook_id = 'Test' to 'Hij', incrementing times_played 
by one and times_won by one:  
    update_player(facebook_id='Test', last_name='Hij', times_played=1, times_won=1, sex = 'Male')    
    
- adding a conversation to the user with facebook_id = 'Test', message_content = 'Test message', said by the user at the very moment with a 'happy' message_intent:  
    add_conversation(facebook_id='Test', who_said_it=True, message_content='Test message', message_intent='happy',
                 message_timestamp=datetime.datetime.now())    
                 
- printing the first name of the facebook_id='Test' player         
    print(find_player('Test').first_name)    

- printing all of the conversations message_content of facebook_id='Test' player:  
player_conversations = find_player('Test').conversations  
for conversation in player_conversations : print(conversation.message_content)
