import RPi.GPIO as GPIO
import sys
import serial
import time
import requests
import json
import glob
from time import sleep, strftime
from subprocess import *
from datetime import datetime
global serialport

sensorPin = 7

GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensorPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

global timeTest  # this is used for the interrupt
# display function takes 16 seconds to run so 38*16 = 608s or about 10m until display goes to sleep after motion stops.
timeTest = 38

LCD = serial.Serial('/dev/ttyAMA0', 19200)


def display():
    LCD.write('\x0E\x0C')  # clears display
    LCD.write(datetime.now().strftime('%b %d %H:%M:%S\n'))
    # time.sleep(3)
    LCD.write('\x10\x0D')  # 2nd line on display
    LCD.write('Getting Ready')
    time.sleep(8)  # pause 8 seconds

    LCD.write('\x0E\x0C')
    LCD.write("First line")
    LCD.write('\x0A\x0D')
    LCD.write("Second line")
    sleep(8)


def resetTimeTest(self):  # function called by interrupt in another thread (requires timeTest to be global to still use here?)
    global timeTest
    timeTest = 38
    return


LCD.open()
LCD.write('\x0E\x0C')  # clears display \x0C
LCD.write("hello & welcome")

GPIO.add_event_detect(sensorPin, GPIO.RISING, callback=resetTimeTest,
                      bouncetime=40)  # interrupt for PIR sensor

while 1:
    if (timeTest > 0):
        display()  # display isn't asleep until time runs out. time is reset to 10m (38) or whatever by PIR sensor if motion is detected
    else:
        LCD.write('\x0E\x0C')
        LCD.write("sleeping.....")

    timeTest = timeTest - 1
    # this main loop runs on a 1s basis with display() taking 16s during every call.
    sleep(1)

LCD.close()
