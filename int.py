#!/usr/bin/env python3

import http.client, urllib.parse
import thingspeak, Adafruit_DHT
#import digitalio, busio, adafruit_bmp280
import time


key = 'OL32V7QUCKN8Y4NU'


def int():
    #extract CPU temperature from pi control csv file CORETEMP
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

    params = urllib.parse.urlencode({'field1': temp, 'field2': freq, 'field3': cpuload, 'field4': ram, 'key':key })
    headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = http.client.HTTPConnection("api.thingspeak.com:80")
    
    conn.request("POST", "/update", params, headers)
    response = conn.getresponse()
            
    print (temp)
    print (freq)
    print (cpuload)
    print (ram)
    print (response.status, response.reason)
    data = response.read()
    conn.close()

    
int()
            
