import json


for i in range(0,66):
    json.load(open("../rest/billboard-data/years2/{0}.json".format(str(1950+i))))
    json.dump(open("../rest/billboard-data/combined.json"))
