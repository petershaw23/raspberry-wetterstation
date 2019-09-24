#!/usr/bin/env python3
# new version 2019. only one sensor, bosch bme280
from datetime import datetime
import time
Datum = datetime.now().strftime('%-d.%-m.')
Uhrzeit = datetime.now().strftime('%H:%M')
print (Datum, Uhrzeit)
#time.sleep(20) #kann geloescht werden, nur bei benutzung mit crontab @reboot machts sinn
import http.client, urllib.parse


# import board # old?
# import busio # old?
import bme280
import smbus2
import json
import requests
import math
#import statistics

key = 'UUIR9GYRF0SQ2SQU' #der thingspeak write key

# konstanten fuer taupunkt berechnung:
A = 17.27
B = 237.7


#BME 280
port = 1
address = 0x76 # Adafruit BME280 address. Other BME280s may be different
bus = smbus2.SMBus(port)
bme280.load_calibration_params(bus,address)

def ext():
    #bme280 read values
    bme280_data = bme280.sample(bus,address)
    
    bmetempRaw = bme280_data.temperature
    bmetemp = "%.3f" % bmetempRaw #rundet mit 3 trailing zeros, z.B. 23,300 °C
    
    humidityRaw = bme280_data.humidity
    humidity = "%.1f" % humidityRaw #rundet mit 1 trailing zeros, z.B. 51,0 %
    
    luftdruckRaw = bme280_data.pressure
    luftdruck = "%.3f" % luftdruckRaw #rundet mit 3 trailing zeros, z.B. 1005,542 hpA

    #taupunkt
    alpha = ((A * bmetempRaw) / (B + bmetempRaw)) + math.log(humidityRaw/100.0)
    taupunktRaw = (B * alpha) / (A - alpha)
    taupunkt = "%.1f" % taupunktRaw
    
    
    # d1 mini data
    data2 = requests.get(url="https://api.thingspeak.com/channels/843073/feeds.json?results=1")
    jsonobj2 = json.loads(data2.content.decode('utf-8'))
    tempD1 = (jsonobj2["feeds"][0]["field1"])
    humiD1 = (jsonobj2["feeds"][0]["field2"])
    
    deltaT = round(float(bmetemp) - float(tempD1), 3)
    deltaH = round(float(humidity) - float(humiD1), 3)
    #taupunktD1
    #alphaD1 = ((A * tempD1) / (B + tempD1)) + math.log(humiD1/100.0)
    #taupunktRawD1 = (B * alphaD1) / (A - alphaD1)
    #taupunktD1 = "%.1f" % taupunktRawD1
    
    #write to thingspeak via urllib
    params = urllib.parse.urlencode({'field1': deltaT, 'field2': deltaH, 'field3': bmetemp, 'field4': taupunktD1, 'field5': humidity, 'field6': taupunkt, 'field7': luftdruck, 'key':key })
    headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = http.client.HTTPConnection("api.thingspeak.com:80")
    conn.request("POST", "/update", params, headers)
    response = conn.getresponse()
    print ('bme temp: ' +str(bmetemp) +' rounded from: ' +str(bmetempRaw))
    print ('bme humi:  '+str(humidity)+' rounded from: '+str(humidityRaw))
    print ('luftdruck: '+str(luftdruck)+' rounded from: '+str(luftdruckRaw))
    print ('taupunkt:  '+str(taupunkt) +' rounded from: '+str(taupunktRaw))
    print ('tempD1:   '+str(tempD1)+' rounded from: '+str(tempD1))
    print ('humiD1:   '+str(humiD1)+' rounded from: '+str(humiD1))
    #print ('taupunktD1:'+str(taupunktD1) +' rounded from: '+str(taupunktRawD1))
    print ('deltaT:   '+str(deltaT)+' rounded from: '+str(deltaT))
    print ('deltaH:   '+str(deltaH)+' rounded from: '+str(deltaH))
    
    print (response.status, response.reason)
    data = response.read()
    conn.close()


ext()
            

