#!/usr/bin/env python
import Adafruit_CharLCDPlate
import time
from time import sleep
import events

lcd = Adafruit_CharLCDPlate

class MyClass(object):
	def __init__(self):
		self.anevent = EventHandler(self)
		
def myEvent(sender):
	lcd.clear()
	lcd.message("Event Handled")
	sleep(5)
	lcd.clear()
	lcd.message("Blink")
	sleep(3)
	lcd.clear()
	
def loop():
	myobj = MyClass()
	myobj.anevent += myEvent
	while True:
		line = raw_input("HI")
		if line == "True":
			myobj.anevent()


loop()
		
		

	
		

