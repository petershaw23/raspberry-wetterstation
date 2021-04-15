## collect data from vnstat and send it to thingspeak #####
## script by peter shaw - https://github.com/petershaw23/ #
## dependencies: vnstat (sudo apt install vnstat) #########
## tested with vnstat version 1.18 on raspbian buster #####
## use case: cronjob every day at 23:59h ##################

#!/usr/bin/env python3

import os
import subprocess
import http.client
import urllib.parse
import requests
import json

key = 'XXXXXXXXXX' #Thingspeak API write key of your thingspeak channel

vnstat = subprocess.getoutput("vnstat -i eth0 --json") #generate vnstat json as text output
#print (vnstat) # for debugging, plain output
jsonobj = json.loads(vnstat) # convert text output to json object
rx = int((jsonobj["interfaces"][0]["traffic"]["days"][0]["rx"])/1024) # read json rx of today, convert to MB
tx = int((jsonobj["interfaces"][0]["traffic"]["days"][0]["tx"])/1024) # read json tx of today, convert to MB
rxAvg = int(rx * 1024 / 24 / 60 / 60) # calculate average kb/sec for the day
txAvg = int(tx * 1024 / 24 / 60 / 60) #                "

# debugging:
print ('rx: '+str(rx)+str(' MB received today'))
print ('tx: '+str(tx)+str(' MB transmitted today'))
print ('rxAvg: '+str(rxAvg)+str(' kb/sec'))
print ('txAvg: '+str(txAvg)+str(' kb/sec'))

# write new values to thingspeak
params = urllib.parse.urlencode({'field1': rx, 'field2': tx, 'field3': rxAvg, 'field4': txAvg, 'key':key }) # change field numbers accordingly
headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
conn = http.client.HTTPConnection("api.thingspeak.com:80")
conn.request("POST", "/update", params, headers)
response = conn.getresponse()
print (response.status, response.reason)
data = response.read()
conn.close() 
