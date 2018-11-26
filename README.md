___ProjectWiki_______________________________________

Flask    stawia lokalnie stronke i obsługuje GET i POST
ngrok    żeby udostępnic lokalną stronke do testow online

Info:
'code'			zawiera
'resources'		zawiera materiały potrzebne do funkcjonowania: grafiki, słowniki itp.
	'ngrok.exe'	appka do postawienia serwera w siecie na czas testów (8h)
'tests'			zawiera
'data'			bazy danych(?)
'ChatBotGame.py'	faktyczna applikacja
'__init__'		https://stackoverflow.com/questions/448271/what-is-init-py-for

___HowToRun_______________________________________
1. odpal 'ChatBotGame.py'
2. odpal ngrok.exe
3. w oknie ngrok wpisz: ngrok http 5000
   (lub inny numer bedacy koncowka adresu local host z pkt1)
4. skopiuj Forwarding https... do Facebook developers
   np. https://280e58b1.ngrok.io

___TODO_____________________________________________
*moved todo to github project tasks*
