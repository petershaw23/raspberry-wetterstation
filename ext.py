#!/usr/bin/env python3

import http.client, urllib.parse
import thingspeak, Adafruit_DHT
import board
import busio
import adafruit_bmp280
import time

key = 'UUIR9GYRF0SQ2SQU'

# fuer taupunkt:
A = 17.27
B = 237.7
import math


# fuer dht22:
pinDHT = 27
sensorDHT = Adafruit_DHT.DHT22

#fuer BMP 280 luftdrucksensor
i2c = busio.I2C(board.SCL, board.SDA)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
#change this to match the location's pressure (hPa) at sea level
bmp280.sea_level_pressure = 1013.25

def ext():
    #Kabel Temp Sensor 1
    tempfileex1 = open("/sys/bus/w1/devices/28-02131dc072aa/w1_slave")
    thetext01 = tempfileex1.read()
    tempfileex1.close()
    tempdataex1 = thetext01.split("\n")[1].split(" ")[9]
    temperatureex1 = float(tempdataex1[2:])
    temperatureex1 = temperatureex1 / 1000
    #temperatureex1 = 20 falls wackelkontakt
    tempex1 = temperatureex1

    #Kabel Temp Sensor 2
    tempfileex2 = open("/sys/bus/w1/devices/28-011432f02f58/w1_slave")
    thetext02 = tempfileex2.read()
    tempfileex2.close()
    tempdataex2 = thetext02.split("\n")[1].split(" ")[9]
    temperatureex2 = float(tempdataex2[2:])
    temperatureex2 = temperatureex2 / 1000
    tempex2 = temperatureex2

    #bmp280.temperature
    bmptemp = bmp280.temperature
	
	#DHT22 script
    humidity22, temperature22 = Adafruit_DHT.read_retry(sensorDHT, pinDHT)
        
    #taupunkt
    alpha = ((A * temperature22) / (B + temperature22)) + math.log(humidity22/100.0)
    taupunkt = (B * alpha) / (A - alpha)

    #luftdruck
    luftdruck = bmp280.pressure
    
	
	

    params = urllib.parse.urlencode({'field1': tempex1, 'field2': tempex2, 'field3': bmptemp, 'field4': temperature22, 'field5': humidity22, 'field6': taupunkt, 'field7': luftdruck, 'key':key })
    headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = http.client.HTTPConnection("api.thingspeak.com:80")
    
    conn.request("POST", "/update", params, headers)
    response = conn.getresponse()
            
    print (tempex1)
    print (tempex2)	    
    print (bmptemp)
    print (temperature22)
    print (humidity22)
    print (taupunkt)
    print (luftdruck)
    print (response.status, response.reason)
    data = response.read()
    conn.close()

    
ext()
            
