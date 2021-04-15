
import os
import subprocess
import json
vnstat = subprocess.getoutput("vnstat -i eth0 --json")
#print (vnstat) # for debugging
jsonobj = json.loads(vnstat)
rx = int((jsonobj["interfaces"][0]["traffic"]["days"][0]["rx"])/1024) #read json rx of today, convert to MB
tx = int((jsonobj["interfaces"][0]["traffic"]["days"][0]["tx"])/1024)  #read json tx of today, convert to MB
rxAvg = int(rx * 1024 / 24 / 60 / 60) #calculate average kb/sec for one day
txAvg = int(tx * 1024 / 24 / 60 / 60) #                "
print ('rx: '+str(rx)+str(' MB received today'))
print ('tx: '+str(tx)+str(' MB transmitted today'))
print ('rxAvg: '+str(rxAvg)+str(' kb/sec'))
print ('txAvg: '+str(txAvg)+str(' kb/sec'))
