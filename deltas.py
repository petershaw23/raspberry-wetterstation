!/usr/bin/python3
import json
import requests
import http.client, urllib.parse
# pi1 data
data1 = requests.get(url="https://api.thingspeak.com/channels/647418/feeds.json?results=1")
jsonobj1 = json.loads(data1.content.decode('utf-8'))
tempPi1 = (jsonobj1["feeds"][0]["field3"])
humiPi1 = (jsonobj1["feeds"][0]["field5"])


# d1 mini data
data2 = requests.get(url="https://api.thingspeak.com/channels/843073/feeds.json?results=1")
jsonobj2 = json.loads(data2.content.decode('utf-8'))
tempD1 = (jsonobj2["feeds"][0]["field1"])
humiD1 = (jsonobj2["feeds"][0]["field2"])



deltaT = round(float(tempPi1) - float(tempD1), 3)
deltaH = round(float(humiPi1) - float(humiD1), 3)

print ('Pi1: temp '+str(tempPi1)+'  humidity: '+str(humiPi1))
print ('D1: temp '+str(tempD1)+'  humidity: '+str(humiD1))
print ('Delta T: '+str(deltaT))
print ('Delta H: '+str(deltaH))
if deltaT > 1:
    print ('Lüften! Draussen ist es kälter!')
if deltaH > 2:
    print ('Lüften! Draussen ist es trockener!')


#write deltas to thingspeak channel

key = 'KGXTB1D2NUPP4G5T' #dein thingspeak write key

#write to thingspeak via urllib
params = urllib.parse.urlencode({'field4': deltaT, 'field5': deltaH, 'key':key })
headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
conn = http.client.HTTPConnection("api.thingspeak.com:80")
conn.request("POST", "/update", params, headers)
response = conn.getresponse()
print (response.status, response.reason)
   
data = response.read()
conn.close()
