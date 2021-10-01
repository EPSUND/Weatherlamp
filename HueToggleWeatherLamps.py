#!usr/bin/python3
from phue import Bridge
import requests
import re
from bs4 import BeautifulSoup
import time

#Hue constants
TEMPERATURE_LAMP_NAME = "Hue color candle 4"
TEMP_COLOR = []
TEMP_COLOR.append([0.678, 0.3165])#30+
TEMP_COLOR.append([0.6329, 0.3523])
TEMP_COLOR.append([0.5796, 0.3923])
TEMP_COLOR.append([0.5388, 0.4347])
TEMP_COLOR.append([0.5006, 0.4517])
TEMP_COLOR.append([0.4781, 0.4686])
TEMP_COLOR.append([0.4138, 0.4258])
TEMP_COLOR.append([0.3788, 0.3936])
TEMP_COLOR.append([0.3458, 0.3711])
TEMP_COLOR.append([0.3035, 0.3353])
TEMP_COLOR.append([0.2372, 0.3015])#0
TEMP_COLOR.append([0.2071, 0.2699])
TEMP_COLOR.append([0.1806, 0.2432])
TEMP_COLOR.append([0.1625, 0.2089])
TEMP_COLOR.append([0.1566, 0.1699])
TEMP_COLOR.append([0.1433, 0.1173])
TEMP_COLOR.append([0.1545, 0.0993])#15-
#Weather constants and functions
WEATHER_DATA_FORMAT = ".xml"
TEMPERATURE_RANGE = 45.0
def createTempList():
    tempStep = TEMPERATURE_RANGE / len(TEMP_COLOR)
    temps = []
    temps.append(30.0)
    for i in range(1, len(TEMP_COLOR)):
        temps.append(temps[i - 1] - tempStep)
    return temps 
TEMP_LIST = createTempList()
TEMPERATURE_URL = "https://opendata-download-metobs.smhi.se/api/version/latest/parameter/1/station/97530/period/latest-hour/data" #Uppsala airport
def getTempColorIndex(temperature):
    for i in range(len(TEMP_LIST)):
        if(temperature >= TEMP_LIST[i]):
            return i
    return len(TEMP_LIST) - 1 

#Make request to SMHI API to get temperature
request = requests.get(TEMPERATURE_URL + WEATHER_DATA_FORMAT)
soup = BeautifulSoup(request.content, "html.parser")
#Parse the request data and get the temperaure 
temperature = float(soup.value.value.string)

#Get session
session = requests.Session()
#Get ip address of phillips hue bridge
request = session.get("https://discovery.meethue.com")
respText = request.text
matches = re.search('\"internalipaddress\"\:\"(.+?)\"', respText)
bridgeIp = matches.group(1)

#Connect to bridge
bridge = Bridge(bridgeIp)
bridge.connect()

lights = bridge.lights

# Set the right color for the temperature
for l in lights:
    if TEMPERATURE_LAMP_NAME == l.name:
        l.xy = TEMP_COLOR[getTempColorIndex(temperature)]
print("Temperature " + str(temperature) + " recorded. Lamp color updated")
