
#!/usr/bin/env python3
#this script extracts data from logs written by "pi-control", which you can get here:
#https://pi-control.de/ 
import http.client, urllib.parse
#import thingspeak

key = 'OL32V7QUCKN8Y4NU' #Thingspeak API write key


def int():
    #temp
    tFileT = open('/sys/class/thermal/thermal_zone0/temp')
    tempRaw = float(tFileT.read())
    temp = tempRaw/1000
    tFileT.close()
    
    #freq
    tFileF = open('/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq')
    freqRaw = float(tFileF.read())
    freq = freqRaw/1000
    tFileF.close()
    
    

    #extract cpuload
    #inputfile4 = "/var/www/html/resources/log/statistic/cpuload.csv"
    #with open(inputfile4, "r") as i:
    #    for line in i: pass
    #    cpuload = line[11:]

    #extract ram
    #inputfile5 = "/var/www/html/resources/log/statistic/ram.csv"
    #with open(inputfile5, "r") as j:
    #    for line in j: pass
    #    ram = line[11:]

    params = urllib.parse.urlencode({'field1': temp, 'field2': freq, 'key':key })
    headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = http.client.HTTPConnection("api.thingspeak.com:80")
    
    conn.request("POST", "/update", params, headers)
    response = conn.getresponse()
    #for debugging:
    print (temp)
    print (freq)
    #print (cpuload)
    #print (ram)
    print (response.status, response.reason)
    
    data = response.read()
    conn.close()

    
int()
            
