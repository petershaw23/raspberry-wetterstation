#!/usr/bin/env python
import httplib, urllib, thingspeak, time

# lib fuer DHT22 sensor luftfeuchtigkeit
import Adafruit_DHT

# lib fuer bmp280 sensor luftdruck (laed adafruit "CircuitPython" und "bmp280" libraries)
import board, busio, adafruit_bmp280

# lib fuer taupunktberechnung:
import math




#konstanten fuer taupunktberechnung
A = 17.27
B = 237.7

# festlegungen fuer dht22:
pinDHT = 27
sensorDHT = Adafruit_DHT.DHT22

# festlegungen fuer BMP280
i2c = busio.I2C(board.SCL, board.SDA)
sensorBMP = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
sensorBMP.sea_level_pressure = 1016.5

#channel write key fuer thingspeak
key = '83N9AKFZ0QUCMO7M'

#intervall des scripts
sleep = 120

def ext():
   while True:
       	
	#Kabelsensor 1
 	tempfileex1 = open("/sys/bus/w1/devices/28-02131dc072aa/w1_slave")
        thetext01 = tempfileex1.read()
        tempfileex1.close()
        tempdataex1 = thetext01.split("\n")[1].split(" ")[9]
        temperatureex1 = float(tempdataex1[2:])
        temperatureex1 = temperatureex1 / 1000
        kabel1 = temperatureex1

	#Kabelsensor 2
 	tempfileex2 = open("/sys/bus/w1/devices/28-011432f02f58/w1_slave")
        thetext02 = tempfileex2.read()
        tempfileex2.close()
        tempdataex2 = thetext02.split("\n")[1].split(" ")[9]
        temperatureex2 = float(tempdataex2[2:])
        temperatureex2 = temperatureex2 / 1000
        kabel2 = temperatureex2

	#Temperature DHT und Luftfeuchtigkeit DHT
	humidityDHT, temperatureDHT = Adafruit_DHT.read_retry(sensorDHT, pinDHT)
	
	#taupunktberechnung
	alpha = ((A * temperatureDHT) / (B + temperatureDHT)) + math.log(humidityDHT/100.0)
	taupunkt = (B * alpha) / (A - alpha)

	#luftdruck, temperatur, hoehe BMP
	luftdruck = sensorBMP.pressure
	temperatureBMP = sensorBMP.temperature
	hoehe = sensorBMP.altitude

        params = urllib.urlencode({'field1': kabel1, 'field2': kabel2, 'field3': temperatureDHT, 'field4': temperatureBMP, 'field5': humidityDHT, 'field6': taupunkt, 'field7': luftdruck, 'field8': hoehe, 'key':key })
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")
        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            
	    print 'kabel1 = 		{0:0.2f} deg C'.format(kabel1)
	    print 'kabel2 = 		{0:0.2f} deg C'.format(kabel2)
	    print 'temperatureDHT = {0:0.2f} deg C'.format(temperatureDHT)	    
	    print 'temperatureBMP = {0:0.2f} deg C'.format(temperatureBMP)
	    print 'humidityDHT = 	{0:0.2f} % rel'.format(humidityDHT)
	    print 'taupunkt = 		{0:0.2f} deg C'.format(taupunkt)
	    print 'luftdruck = 		{0:0.2f} Luftfeuchtigkeit %'.format(luftdruck)
		print 'hoehe = 			{0:0.2f} m ueber Meeresspiegel'.format(hoehe)
            print response.status, response.reason
            data = response.read()
            conn.close()
        except:
            print "connection failed"
        break
#sleep for desired amount of time
if __name__ == "__main__":
        while True:
                ext()
                time.sleep(sleep)