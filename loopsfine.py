#!/usr/bin/env python

from time import sleep
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
lcd = Adafruit_CharLCDPlate()

def errorHandler(error):
	for x in range(0,4):
		lcd.clear()		
		print str(error)
		sleep(.5)
		print ""		
		sleep(.5)
		lcd.message("Error")
		sleep(.5)
		

def mainloop():
	while True:
		try:
			number = raw_input("Input a number:")
			result = (10 / int(number))
			print result 
		except Exception as e:
			errorHandler(e)
			pass
			
mainloop()
		
	
