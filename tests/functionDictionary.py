#Set of responses for particular intents:
def responder(intent, user_message="", userid="", bot=""):
    switcher = {
        "test1":    test1,
        "test2":    test2
    }
    # Get the function from switcher dictionary
    #func = switcher.get(intent, lambda user_message, userid, bot : default_message)
    func = switcher.get(intent, default_message)
    # Execute the function
    return func(user_message, userid, bot)

def default_message(user_message, userid="", bot=""):
    print('cotusiedzieje')
    print('232132312312331223132')
    return ["odpnatestdefault"]

def test1(user_message, userid="", bot=""):
    a=2+2
    print(a)
    return ["odpnatest1"]

def test2(user_message, userid="", bot=""):
    return ["odpnatest2"]


r1 = responder('test1','tresc wiadomosci','023134','342324')
r2 = responder('test2','tresc wiadomosci','023134','342324')
r3 = responder('default_message','tresc wiadomosci','023134','342324')

print(r1)
print(r2)
print(r3)
