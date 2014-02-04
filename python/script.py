# (c) 2013 Roberto Giungato - GPLv2
# Imports
import json
import webiopi
import time
from time import sleep
import datetime
import sys
import subprocess
import re
import requests
import urllib.parse
import urllib.request
import os

from ctypes import c_short
sys.path.append("/root/sermig/html")

# Enable debug output
webiopi.setDebug()

from webiopi.devices.sensor import DS18B20
temp0 = DS18B20(slave="28-0000050364ee") 

from webiopi.devices.analog import MCP3008
adc = MCP3008(chip=0)

# Retrieve GPIO lib
GPIO = webiopi.GPIO

LED0 = 17
RELAY1 = 2
RELAY2 = 3

global Temp0
Temp0 = 0
global Lum0
Lum0 = 0
global Lum0i
Lum0i = 0
global sleep0
sleep0 = 0

# Called by WebIOPi at script loading
def setup():
    webiopi.debug("Blink script - Setup")
    # Setup GPIOs

    GPIO.setFunction(LED0, GPIO.OUT)
    GPIO.setFunction(RELAY1, GPIO.OUT)
    GPIO.setFunction(RELAY2, GPIO.OUT)

#------------------------------------------------------------------
def get_DS18B20_Temperature():
    global Temp0   
#, Temp1, Temp2, Temp3, Temp4, Temp5, Temp6, Temp7
    try:
        Temp0 = "%.2f" % (temp0.getCelsius())
        print (Temp0)
        return Temp0
    except (IOError, TypeError):
        print ("ERROR getting temp")
        pass
#------------------------------------------------------------------

def get_luminosity():
	global Lum0
	global Lum0i
	try:
		Lum0i = adc.analogReadVolt(0)
		Lum0 = "%.2f" % (adc.analogReadVolt(0))
		print (Lum0)
	except (IOError, TypeError):
		print ("ERROR getting lum")
	pass


def send_temp_nimbits():
        global Temp0
        data = {"email":"rgiungato@gmail.com",
                "key":"lightkey",
                "point":"sermigTempi",
        "value":Temp0}

        try:
                r = requests.post("http://cloud.nimbits.com/service/value", data=data)
                print ("Temp sent to Nimbits")
        except:
                print ("ERROR sending temp to Nimbits")
        pass

def send_lum_nimbits():
        global Lum0
        data = {"email":"rgiungato@gmail.com",
                "key":"lightkey",
                "point":"sermigLight",
        "value":Lum0}

        try:
                r = requests.post("http://cloud.nimbits.com/service/value", data=data)
                print ("Lum sent to Nimbits")
        except:
                print ("ERROR sending lum to Nimbits")
        pass


# Looped by WebIOPi
def loop():
	global sleep0
	# Toggle LED without sleeping
	value = not GPIO.digitalRead(LED0)
	if (sleep0 == 10000):
		GPIO.digitalWrite(LED0, value)
		sleep0 = 0
	else:
		sleep0 = sleep0 + 1

	if (Lum0i > 3):
		GPIO.digitalWrite(RELAY1, GPIO.HIGH)
	else:
		GPIO.digitalWrite(RELAY1, GPIO.LOW)

#	webiopi.sleep(3)


# Called by WebIOPi at server shutdown
def destroy():
    webiopi.debug("Blink script - Destroy")
    # Reset GPIO functions
    GPIO.digitalWrite(LED0, GPIO.LOW)
    GPIO.digitalWrite(RELAY1, GPIO.LOW)
    GPIO.digitalWrite(RELAY2, GPIO.LOW)
    GPIO.setFunction(LED0, GPIO.IN)
    GPIO.setFunction(RELAY1, GPIO.IN)
    GPIO.setFunction(RELAY2, GPIO.IN)

# Macro called by WebIOPi to retreve 7off DS18B20 Temp sensors and DH11 Temp/Humidity sensor
@webiopi.macro
def Temp(arg0):
    get_DS18B20_Temperature()
    send_temp_nimbits()
    return ("%s" % (Temp0))

# Macro called by WebIOPi to retreve the state of GPIO17
@webiopi.macro
def GETPIO(arg0):
    g0 = (int(GPIO.digitalRead(17)))
    return ("%s" % (g0))

@webiopi.macro
def Lum(arg0):
	get_luminosity()
	send_lum_nimbits()
	return ("%s" % (Lum0))

@webiopi.macro
def sendLum(arg0):
	get_luminosity()
	send_lum_nimbits()
	return ("%s" % (Lum0))

@webiopi.macro
def Servo1(arg0):
	os.system("echo \"23=0.1\" > /dev/pi-blaster")
	sleep(2)
	os.system("echo \"23=0.2\" > /dev/pi-blaster")
	os.system("echo \"23=0\" > /dev/pi-blaster")
	return ("%s" % ("done"))
