___ProjectWiki_______________________________________

Info:
- 'code'			contains all the neccesarry methods and classes
- 'resources'		contains all media like json dictionaries, graphics, etc.
- 'tests'			set of tests written for particular parts of the app
- 'ChatBotGame.py'	the app itselfs
- '__init__'		to treat repo as a library https://stackoverflow.com/questions/448271/what-is-init-py-for
- TODO			tasks to be done can be found in Github/Projects/Todo

Modules:
- Flask  deploys local website to handle GET and POST
- ngrok.exe    deploys local server to http for limited time of testing


___HowToRun_______________________________________
1. run 'ChatBotGame.py'
2. run ngrok.exe
3. in the ngrok console type: ngrok http 5000
   (or other end of local host address)
4. copy 'Forwarding https...' and paste on Facebook developers website (e.g. https://280e58b1.ngrok.io)
