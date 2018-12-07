#!/usr/bin/env python

import httplib, urllib, thingspeak
import time


sleep = 120
key = 'OL32V7QUCKN8Y4NU'

def int():
   while True:
    
	#extract CPU temperature from pi control csv file CORETEMP
	inputfile1 = "/var/www/html/resources/log/statistic/coretemp.csv"
	with open(inputfile1, "r") as f:
		for line in f: pass
		CPUtemp = line[11:]

	#extract freq
	inputfile3 = "/var/www/html/resources/log/statistic/cpufrequency.csv"
	with open(inputfile3, "r") as h:
		for line in h: pass
		CPUfreq = line[11:]

	#extract cpuload
	inputfile4 = "/var/www/html/resources/log/statistic/cpuload.csv"
	with open(inputfile4, "r") as i:
		for line in i: pass
		CPUload = line[11:]

	#extract ram
	inputfile5 = "/var/www/html/resources/log/statistic/ram.csv"
	with open(inputfile5, "r") as j:
		for line in j: pass
		ram = line[11:]

        params = urllib.urlencode({'field1': CPUtemp, 'field2': CPUfreq, 'field3': CPUload, 'field4': ram, 'key':key })
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")
        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            
	    print 'CPUtemp = {0:0.2f} deg C'.format(temp)    
	    print 'freq = {0:0.2f} mhz'.format(freq)
	    print 'cpuload = {0:0.2f} % CPU'.format(cpuload)
	    print 'ram = {0:0.2f} % RAM used'.format(ram)
            print response.status, response.reason
            data = response.read()
            conn.close()
        except:
            print "connection failed"
        break
#sleep for desired amount of time
if __name__ == "__main__":
        while True:
                int()
                time.sleep(sleep)