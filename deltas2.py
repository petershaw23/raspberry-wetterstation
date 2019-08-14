#!/usr/bin/python3
import json
import requests

# pi1 data
data1 = requests.get(url="https://api.thingspeak.com/channels/647418/feeds.json?results=1")
jsonobj1 = json.loads(data1.content)
#print (jsonobj1)



# d1 mini data
data2 = requests.get(url="https://api.thingspeak.com/channels/647418/feeds.json?results=1")
jsonobj2 = json.loads(data2.content)
#print (jsonobj2)


#depart = (jsonobj["routes"][0]["legs"][0]["arrival_time"]["text"])
