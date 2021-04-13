
#!/usr/bin/env python3
import http.client
import urllib.parse
import psutil
import requests
import json

key = 'XXXXXXX' #Thingspeak API write key


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
    #cpuload
    cpuload = psutil.cpu_percent()
    #ram
    ram = psutil.virtual_memory()[2]
    #downloaded via lan ##NEW PART START############################################
    with open("/proc/net/dev") as f:
        content = f.readlines()
    content = [x.strip() for x in content] 
    #print (content[3]) #check if correct device, should read "eth0 ..."
    lan = str(content[3]).split()
    rxraw = int(lan[1])
    #print (rxraw)
    rxMB = round((rxraw / 1024 / 1000),6)
    print (rxMB)
    # data from thingspeak
    data = requests.get(url="https://api.thingspeak.com/channels/646236/feeds.json?results=1") #change to your channel!
    jsonobj = json.loads(data.content.decode('utf-8'))
    rxMB_old = float(jsonobj["feeds"][0]["field5"])
    print ('rxMB_old: ' +str(rxMB_old))
    last_entry = jsonobj["feeds"][0]["created_at"] #time of last entry
    print ('age of rxMB_old: ' +str(last_entry))
    # calculate deltaT and deltaH
    deltaRX = round(float(rxMB) - float(rxMB_old),6)
    print ('deltaRX: ' +str(deltaRX))
    # calculate kb/sec average in the last 5 minutes
    rxAvg5minRaw = round((deltaRX * 1000 / 300))
    # check if positive value
    num = float(rxAvg5minRaw)
    if num > 0:
        print("Positive number")
        rxAvg5min = rxAvg5minRaw
        print ('average kb/sec: ' +str(rxAvg5min))
    elif num == 0:
        print("Zero")
        rxAvg5min = rxAvg5minRaw
        print ('average kb/sec: ' +str(rxAvg5min))
    else:
        print("Negative number")
        rxAvg5min = 55
        print ('average kb/sec: ' +str(rxAvg5min))
    ##NEW PART END#################################################################
    # now write new values to thingspeak
    params = urllib.parse.urlencode({'field1': temp, 'field2': freq, 'field3': cpuload, 'field4': ram, 'field5': rxMB, 'field6': deltaRX, 'field7': rxAvg5min, 'key':key })
    headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = http.client.HTTPConnection("api.thingspeak.com:80")
    conn.request("POST", "/update", params, headers)
    response = conn.getresponse()
    #for debugging:
    print (temp)
    print (freq)
    print (cpuload)
    print (ram)
   
    print (response.status, response.reason)
    data = response.read()
    conn.close() 
int()
