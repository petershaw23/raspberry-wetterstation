# raspberry-wetterstation
Wetterstation: Raspberry Pi -> Python -> Thingspeak

int.py: Die internen system-stats  werden über die von "pi control" (https://pi-control.de/) erstellten csv dateien ausgelesen.

ext.py: Der Sensor bme280 wird ausgelesen (temp, humidity, air pressure)

beides sendet die daten über die thingspeak API an einen thingspeak channel


multichart.html:  Webpage Javascript to chart multiple ThingSpeak channels on two axis with navigator, load historical data, and export cvs data. // Public Domain, by turgo.
