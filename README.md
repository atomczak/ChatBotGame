___ProjectWiki_______________________________________

Info:
- 'code' - contains all the neccesarry methods and classes
- 'resources' - contains all media like json dictionaries, graphics, etc.
- 'tests' - set of tests written for particular parts of the app
- 'ChatBotGame.py' - the app itselfs
- '__init__' - to treat repo as a library https://stackoverflow.com/questions/448271/what-is-init-py-for
- TODO - tasks to be done can be found in Github/Projects/Todo

Modules:
- Flask - deploys local website to handle GET and POST
- ngrok.exe - deploys local server to http for limited time of testing


___HowToRun_______________________________________
1. run 'ChatBotGame.py'
2. run ngrok.exe
3. in the ngrok console type: ngrok http 5000
   (or other end of local host address)
4. copy 'Forwarding https...' and paste on Facebook developers website (e.g. https://280e58b1.ngrok.io)




___mongodb_connection.py_________________________

Place DB_Connection_Data.txt file in the mongodb_connection.py root directory. The content of DB_Connection_Data.txt should be as follows:

username = <database_username>
password = <database_password>
address = <database_address>
database_name = <database_name>


mongodb_connection.py: sample functions

ADDING A USER WITH THE: facebook_id = 'Test', first_name = 'Abc', last_name = 'Efg' and a 'Male':
create_player(facebook_id='Test', first_name='Abc', last_name='Efg', sex='Male')

UPDATING THE LAST NAME OF THE PLAYER WITH facebook_id = 'Test' to 'Hij', INCREMENTING THE times_played 
BY ONE and times_won BY ONE:
update_player(facebook_id='Test', last_name='Hij', times_played=1, times_won=1, sex = 'Male')

ADDING  ACONVERSATION TO THE USER WITH facebook_id = 'Test', message_content = 'Test message', SAID BY THE USER
AT THE VERY MOMENT WITH  a 'happy' message_intent:
add_conversation(facebook_id='Test', who_said_it=True, message_content='Test message', message_intent='happy',
                 message_timestamp=datetime.datetime.now())
                 
PRINTING THE FIRST NAME OF THE facebook_id='Test' PLAYER:
print(find_player('Test').first_name)

PRINTING THE ALL OF THE CONVERSATIONS message_content of facebook_id='Test' PLAYER:
player_conversations = find_player('Test').conversations
for conversation in player_conversations:
    print(conversation.message_content)
