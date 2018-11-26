Wiki: __________________________________________
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



HowToRun: ________________________________________
1. odpal 'ChatBotGame.py'
2. odpal ngrok.exe
3. w oknie ngrok wpisz: ngrok http 5000
   (lub inny numer bedacy koncowka adresu local host z pkt1)
4. skopiuj Forwarding https... do Facebook developers
   np. https://280e58b1.ngrok.io

TODO _______________________________________________
- jak zrobić udawanie że się pisze na fbm? (te trzy kropki)
- rozpoznaj podstawowe intencje
- rozpoznaj kciuka, naklejke, gifa, obrazek
- hasło restartujące gre
- wyślij naklejke
- command line bot do testów
- wyciagnij informacje o graczu (username etc.)
- co umozliwia fb api?
- sposob na zapis danych - baza danych odpowiedzi etc.

POMYSŁY NA GRĘ________________________________________
Połączenie bota z innymi graczami.
Gracz ma pozorną władzę nad przebiegiem rozgrywki, od niego zależy w którą stronę rozwinie się akcja.
Inicjacja poprzez zdanie relacji z wykonania zadania.
Wątpliwości i niedopowiedzenia budują charakter tajemnicy oraz poufności.
Łamigłówki, dylematy moralne, szyfry, koordynacja działań.
Przekazywanie informacji między członkami organizacji.
rebus

POMYSŁY NA FABUŁE GRY________________________________________
Organizacja walcząca z ukrycia ze złem tego świata. Inspiracja m.in. Mr Robot, Anonymous, Kod Da Vinci, Fight Club.
Gracz może poczcuć się częścią czegoś, na co w życiu by się nie odważył.
Porwania.

ZAŁOŻENIA ________________________________________
- Ludzie niechętnie instalują gry i inne aplikacje.
- Ludzie szukają rozrywki na telefon np. na czas dojadu komunikacją. Proste gry jak flappy bird.
- Ludzi intryguje interakcja z botem / sztuczną inteligencją.
- Gra ma zniekształcac granice miedzy gra a swiatem zewnetrznym
- Gracz ma spore pole do zmiany fabuły gry
- W grupie docelowej znajdujdą się osoby posiadające dostęp do messengera, które gustują w escape room/ text games/ klimaty sensacyjne.

KOMERCYJNE ROZWIĄZANIA: _____________________________________
- Manychat.com
- IBM Watson
- Wit.ai
- api.ai
- motion.ai
- chatfuel - sprawdziłem - szybki start, ale potem ciężko podpiąc logike
- Wordnik
- spaCy
- TextBlob

INTERESUJACE ZRODLA _____________________________________-
Instrukcja na polaczenie FB z pythonem:      https://www.twilio.com/blog/2017/12/facebook-messenger-bot-python.html
https://pythonprogramming.net/chatbot-deep-learning-python-tensorflow/
ChatterBot        https://github.com/gunthercox/ChatterBot
