#!/usr/bin/env python
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
import time
from time import sleep
import socket
import pyodbc
import datetime as dt

machineid = socket.gethostname()
lcd = Adafruit_CharLCDPlate()
			
			
def dboperation(operation):
	conn = pyodbc.connect("DSN=WAGODB;UID=sa;PWD=moldex")
	
	

def CheckMachineState():
	conn = pyodbc.connect("DSN=WAGODB;UID=sa;PWD=moldex")
	cursor = conn.execute("select sku, lotnumber from machinestate where machineid = ?", machineid)
	
	row = cursor.fetchone()
	sku = row[0]
	lot = row[1]

	lcd.clear()
	lcd.backlight(Adafruit_CharLCDPlate.TEAL)
	lcd.message("SKU: " + sku + "\nLot: " + lot)
	
	conn.close()
	
def actonbarcode(barcode):
	if len(barcode) == 12:
			lcd.clear()
			lcd.message("Lot Roll Number:\n" + barcode)
			sleep(3)
			conn = pyodbc.connect("DSN=WAGODB;UID=sa;PWD=moldex")
			cursor = conn.execute("{call dbo.LotScan(?, ?, ?)}", machineid, barcode, dt.datetime.now())
			conn.commit()
			lcd.clear()
			lcd.backlight(Adafruit_CharLCDPlate.GREEN)
			lcd.message("SUCCESS!\nLot Updated")			
			conn.close()
			sleep(2)
			lcd.backlight(Adafruit_CharLCDPlate.TEAL)
	

def errorHandler(error):
	conn = pyodbc.connect("DSN=WAGODB;UID=sa;PWD=moldex")
	cursor = conn.execute("{call dbo.LogError(?, ?)}", machineid, str(error))
	conn.commit()
	conn.close()
	for x in range(0,4):
		lcd.clear()
		lcd.backlight(0x01)
		lcd.message("     ERROR")
		sleep(.5)
		lcd.clear()
		lcd.message("\n     ERROR")
		sleep(.5)
		
	print "WTF"	
	return
	
	
def mainloop():
	while True:
		try:
			CheckMachineState()
			barcode = raw_input("Please Scan A Barcode:")
			actonbarcode(barcode)
		except Exception as e:
			errorHandler(e)
			pass
			
			


mainloop()
