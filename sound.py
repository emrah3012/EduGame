# -*- coding: utf-8 -*-
from time import sleep
import RPi.GPIO as GPIO

CONFIG_FILE = "postavke.config" 
SETTINGS_DIR = "Postavke/"

class Sound:
    BUZZER=22
    #GREEN=17
    #RED=27
    GPIO.setwarnings(False)
    flag = 0

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        #GPIO.setup(self.RED, GPIO.OUT) #led crvena
        #GPIO.setup(self.GREEN, GPIO.OUT) #led zelena
        GPIO.setup(self.BUZZER, GPIO.OUT) #buzzer
        

    def sound_bingo(self):
        GPIO.output(self.BUZZER, GPIO.HIGH)
        #GPIO.output(self.GREEN, True)
        sleep(.1)
        GPIO.output(self.BUZZER, GPIO.LOW)
        #GPIO.output(self.GREEN, False)
        sleep(.1)
        GPIO.output(self.BUZZER, GPIO.HIGH)
        #GPIO.output(self.GREEN, True)
        sleep(.1)
        GPIO.output(self.BUZZER, GPIO.LOW)
        #GPIO.output(self.GREEN, False)
        sleep(.1)
        GPIO.output(self.BUZZER, GPIO.HIGH)
        #GPIO.output(self.GREEN, True)
        sleep(.1)
        GPIO.output(self.BUZZER, GPIO.LOW)
        #GPIO.output(self.GREEN, False)
        sleep(.1)
        GPIO.output(self.BUZZER, GPIO.HIGH)
        #GPIO.output(self.GREEN, True)
        sleep(.1)
        GPIO.output(self.BUZZER, GPIO.LOW)
        # GPIO.output(self.GREEN, False)
        sleep(.1)

    def sound_wrong(self):
        GPIO.output(self.BUZZER, GPIO.HIGH)
        #GPIO.output(self.RED, True)
        sleep(.5)
        GPIO.output(self.BUZZER, GPIO.LOW)
        #GPIO.output(self.RED, False)
