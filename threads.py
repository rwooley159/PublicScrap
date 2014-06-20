import threading
import time
from time import sleep
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate



def lcdcontrol():
	global run
	global t1
	global onService
	while run == True:
		while onService == True:
			lcd.message("Hello")
			sleep(1)
			lcd.clear()
			sleep(1)
		while onService == False:
			lcd.clear()	
			lcd.message("Goodbye")
			sleep(1)
			lcd.clear()
		
		
	
		
		


def loop():
	global run
	global t1
	global onService
	line = raw_input("Input a value:")
	
	if line == "False":
		onService = False
		print "Run changed to False"
	if line == "True":
		onService = True
		print "Run changed to True"		
		if not t1.is_alive():
			t1.start()
	
	loop()

lcd = Adafruit_CharLCDPlate()
run = False
onService = False
t1 = threading.Thread(target=lcdcontrol)
loop()


