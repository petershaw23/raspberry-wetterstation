#!/usr/bin/env python3
import time
#time.sleep(20) #kann geloescht werden, nur bei benutzung mit crontab @reboot machts sinn
import http.client, urllib.parse
import thingspeak, Adafruit_DHT
import board
import busio
import adafruit_bmp280
#import statistics

key = 'UUIR9GYRF0SQ2XXX' #dein thingspeak write key

# variablen fuer taupunkt berechnung:
A = 17.27
B = 237.7
import math


# fuer sensor DHT22 (=humidity22 und temperatur22):
pinDHT = 27
sensorDHT = Adafruit_DHT.DHT22

#fuer BMP 280 luftdrucksensor (=bmptemp und luftdruck):
i2c = busio.I2C(board.SCL, board.SDA)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
#change this to match the location's pressure (hPa) at sea level
bmp280.sea_level_pressure = 1013.25

def ext():
    #bmp280 script
    bmptempRaw = bmp280.temperature
    bmptemp = "%.3f" % bmptempRaw #rundet mit 3 trailing zeros, z.B. 23,300 °C
    #DHT22 script
    humidity22Raw, temperature22Raw = Adafruit_DHT.read_retry(sensorDHT, pinDHT)
    humidity22 = "%.1f" % humidity22Raw #rundet mit 1 trailing zeros, z.B. 51,0 %
    temperature22 = "%.1f" % temperature22Raw

    #luftdruck
    luftdruckRaw = bmp280.pressure
    luftdruck = "%.3f" % luftdruckRaw #rundet mit 3 trailing zeros, z.B. 1005,542 hpA

    #mittelwert der temperaturen
    mittelRaw = (bmptempRaw + temperature22Raw) / 2
    mittel = "%.1f" % mittelRaw

    #taupunkt
    alpha = ((A * mittelRaw) / (B + mittelRaw)) + math.log(humidity22Raw/100.0)
    taupunktRaw = (B * alpha) / (A - alpha)
    taupunkt = "%.1f" % taupunktRaw

    #write to thingspeak via urllib
    params = urllib.parse.urlencode({'field3': bmptemp, 'field4': temperature22, 'field5': humidity22, 'field6': taupunkt, 'field7': luftdruck, 'field8': mittel, 'key':key })
    headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = http.client.HTTPConnection("api.thingspeak.com:80")
    conn.request("POST", "/update", params, headers)
    response = conn.getresponse()
    
    #for debugging, print stuff to console:
    print ('bmp temp: ' +str(bmptemp) +' rounded from: ' +str(bmptempRaw))
    print ('temp22:   ' +str(temperature22) +' rounded from: '+str(temperature22Raw))
    print ('humi22:   ' +str(humidity22) +' rounded from: '+str(humidity22Raw))
    print ('taupunkt:  '+str(taupunkt) +' rounded from: '+str(taupunktRaw))
    print ('luftdruck: '+str(luftdruck)+' rounded from: '+str(luftdruckRaw))
    print ('mittelw:   '+str(mittel)+' rounded from: '+str(mittelRaw))
    print (response.status, response.reason)
   
    data = response.read()
    conn.close()


ext()
            
