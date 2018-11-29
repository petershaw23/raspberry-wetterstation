#!/usr/bin/env python
__author__ = 'munnecke'
# This program logs a Raspberry Pi's CPU temperature to a Thingspeak Channel
# To use, get a Thingspeak.com account, set up a channel, and capture the Channel Key at https://thingspeak.com/docs/tutorials/ 
# Then paste your channel ID in the code for the value of "key" below.
# Then run as sudo python pitemp.py (access to the CPU temp requires sudo access)
# You can see my channel at https://thingspeak.com/channels/41518

import httplib, urllib, thingspeak, Adafruit_DHT, math
import time
sleep = 120
key = '83N9AKFZ0QUCMO7M'

# fuer taupunkt:
A = 17.27
B = 237.7



# fuer dht22:
pin = 27
sensor = Adafruit_DHT.DHT22



def thermometer():
   while True:
       	

	#NEUE METHODE! SENSOR 1
 	tempfileex1 = open("/sys/bus/w1/devices/28-02131dc072aa/w1_slave")
        thetext01 = tempfileex1.read()
        tempfileex1.close()
        tempdataex1 = thetext01.split("\n")[1].split(" ")[9]
        temperatureex1 = float(tempdataex1[2:])
        temperatureex1 = temperatureex1 / 1000
        tempex1 = temperatureex1

	#NEUE METHODE! SENSOR 2
 	tempfileex2 = open("/sys/bus/w1/devices/28-011432f02f58/w1_slave")
        thetext02 = tempfileex2.read()
        tempfileex2.close()
        tempdataex2 = thetext02.split("\n")[1].split(" ")[9]
        temperatureex2 = float(tempdataex2[2:])
        temperatureex2 = temperatureex2 / 1000
        tempex2 = temperatureex2

	#DHT22 script
	humidity22, temperature22 = Adafruit_DHT.read_retry(sensor, pin)
	
	#taupunkt
	alpha = ((A * temperature22) / (B + temperature22)) + math.log(humidity22/100.0)
	taupunkt = (B * alpha) / (A - alpha)

	#extract temperature from pi control csv file CORETEMP
	inputfile1 = "/var/www/html/resources/log/statistic/coretemp.csv"
	with open(inputfile1, "r") as f:
		for line in f: pass
		temp = line[11:]

	#extract freq
	inputfile3 = "/var/www/html/resources/log/statistic/cpufrequency.csv"
	with open(inputfile3, "r") as h:
		for line in h: pass
		freq = line[11:]

	#extract cpuload
	inputfile4 = "/var/www/html/resources/log/statistic/cpuload.csv"
	with open(inputfile4, "r") as i:
		for line in i: pass
		cpuload = line[11:]

	#extract ram
	inputfile5 = "/var/www/html/resources/log/statistic/ram.csv"
	with open(inputfile5, "r") as j:
		for line in j: pass
		ram = line[11:]

        params = urllib.urlencode({'field1': temp, 'field2': tempex1, 'field3': temperature22, 'field4': humidity22, 'field5': freq, 'field6': cpuload, 'field7': taupunkt, 'field8': tempex2, 'key':key })
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")
        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            
	    print temp
	    print tempex1
	    print tempex2	    
	    print freq
	    print cpuload
	    print ram
	    print temperature22
	    print humidity22
	    print taupunkt
            print response.status, response.reason
            data = response.read()
            conn.close()
        except:
            print "connection failed"
        break
#sleep for desired amount of time
if __name__ == "__main__":
        while True:
                thermometer()
                time.sleep(sleep)