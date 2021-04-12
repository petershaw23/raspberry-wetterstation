
#!/usr/bin/env python3
import http.client
import urllib.parse
import psutil

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
    
    #downloaded
    with open("/proc/net/dev") as f:
        content = f.readlines()
    content = [x.strip() for x in content] 
    #print (content[3])
    lan = str(content[3]).split()
    rxraw = int(lan[1])
    #print (rxraw)
    rxMB = round((rxraw / 1000 / 1000),1)
    print (rxMB)

    
    params = urllib.parse.urlencode({'field1': temp, 'field2': freq, 'field3': cpuload, 'field4': ram, 'field5': rxMB,'key':key })
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
