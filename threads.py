import threading
import time
from time import sleep
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate



def lcdcontrol():
	global run
	global t1
	while run == True:
		lcd.message("Hello")
		sleep(1)
		lcd.clear()
		sleep(1)
	
	lcd.clear()	
	lcd.message("Goodbye")
	sleep(1)
	lcd.clear()
	while run == False:
		sleep(1)
	lcdcontrol()
		
		


def loop():
	global run
	global t1
	line = raw_input("Input a value:")
	
	if line == "False":
		run = False
		print "Run changed to False"
	if line == "True":
		run = True
		print "Run changed to True"		
		if not t1.is_alive():
			t1.start()
	
	loop()

lcd = Adafruit_CharLCDPlate()
run = False
t1 = threading.Thread(target=lcdcontrol)
loop()


