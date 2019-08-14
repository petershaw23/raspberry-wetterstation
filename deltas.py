import time
import http.client, urllib.parse
import thingspeak
time.sleep(45)
try:
    chPi1 = thingspeak.Channel(647418)
    outRAWPi1 = chPi1.get({'results':1})
    outSplitPi1 = outRAWPi1.split('\"')
    outTempPi1 = outSplitPi1[-18]
    outHumiPi1 = outSplitPi1[-14]

    chD1 = thingspeak.Channel(843073)
    outRAWD1 = chD1.get({'results':1})
    outSplitD1 = outRAWD1.split('\"')
    outTempD1 = outSplitD1[-10]
    outHumiD1 = outSplitD1[-6]


except: #falls offline
    outTempPi1 = '1'
    outHumiPi1 = '1'
    outTempD1 = '1'
    outHumiD1 = '1'


deltaT = round(float(outTempPi1) - float(outTempD1), 1)
deltaH = round(float(outHumiPi1) - float(outHumiD1), 1)

print ('Pi1: temp '+str(outTempPi1)+'  humidity: '+str(outHumiPi1))
print ('D1: temp '+str(outTempD1)+'  humidity: '+str(outHumiD1))
print ('Delta T: '+str(deltaT))
print ('Delta H: '+str(deltaH))
#if deltaT > 1:
#    print ('Lüften! Draussen ist es kälter!')
#if deltaH > 2:
#    print ('Lüften! Draussen ist es trockener!')


#write deltas to thingspeak channel

key = 'KGXTB1D2NUPP4G5T' #dein thingspeak write key

#write to thingspeak via urllib
params = urllib.parse.urlencode({'field4': deltaT, 'field5': deltaH, 'key':key })
headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
conn = http.client.HTTPConnection("api.thingspeak.com:80")
conn.request("POST", "/update", params, headers)
response = conn.getresponse()
print (response.status, response.reason)
   
data = response.read()
conn.close()


