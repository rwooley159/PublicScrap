#!/usr/bin/env python
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
import RPi.GPIO as GPIO
import time
from time import sleep
import socket
import pyodbc
import datetime as dt

# set up machineid
machineid = socket.gethostname()
# set up lcd screen
lcd = Adafruit_CharLCDPlate()

# set up GPIO pin number by name
ontSwitch = 8

# set up a bool value for maintenance
isUnderMaintenance = False


			
			
def dboperation(operation):
	conn = pyodbc.connect("DSN=WAGODB;UID=sa;PWD=moldex")
	
	

def CheckMachineState():
	conn = pyodbc.connect("DSN=WAGODB;UID=sa;PWD=moldex")
	cursor = conn.execute("select sku, lotnumber from machinestate where machineid = ?", machineid)
	
	row = cursor.fetchone()
	conn.close()
	
	sku = row[0]
	lot = row[1]

	lcd.clear()
	lcd.backlight(Adafruit_CharLCDPlate.TEAL)
	lcd.message("SKU: " + sku + "\nLot: " + lot)
	
	
	
def toggleMaintenance(state):
	if state == True:				
		lcd.clear()
		lcd.message("  Maintenance\n      Mode")
		sleep(5)
		while state == True:
			lcd.clear()
			lcd.backlight(Adafruit_CharLCDPlate.RED)
			lcd.message("     UNDER \n  MAINTENANCE")
			sleep(2)
			CheckMachineState()
			sleep(2)				
		else:
			CheckMachineState()
			return 
	
	
	
def actonbarcode(barcode):
	global isUnderMaintenance
	try:
		if len(barcode) == 12:
			# This is a roll of material, update machine with new roll and lot
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
			
		if len(barcode) == 7:
			# This is a SKU Label, update SKU
			lcd.clear()
			lcd.message("SKU:\n" + barcode)
			sleep(3)
			conn = pyodbc.connect("DSN=WAGODB;UID=sa;PWD=moldex")
			cursor = conn.execute("{call dbo.SKU(? , ?)}", machineid, barcode )
			conn.commit()
			lcd.clear()
			lcd.backlight(Adafruit_CharLCDPlate.GREEN)
			lcd.message("SUCCESS!\nSKU Updated")			
			conn.close()
			sleep(2)
			lcd.backlight(Adafruit_CharLCDPlate.TEAL)	
			
		if len(barcode) == 6:
			# This is an employee badge
			lcd.clear()
			lcd.message("Badge ID:\n" + barcode)
			sleep(3)
			
			# Get rid of leading zeroes
			listBadge = list(barcode)			
			while listBadge[0] == '0':
				listBadge.remove(listBadge[0])
			barcode = "".join(listBadge)
			# Now have short badge id
			
			conn = pyodbc.connect("DSN=NovaTime;UID=sa;PWD=moldex")
			cursor = conn.execute("select cfirstname, clastname, cgroup2 from employee where ncardnum = ?", barcode)	
			row = cursor.fetchone()
			firstname = row[0]	
			lastname = row[1]			
			department = row[2]
			conn.close()
			department = department.rstrip()
			department = department.lstrip()			
			
			lcd.clear()
			lcd.message(firstname + "\n" + lastname)
			sleep(2)
			lcd.clear()
			lcd.backlight(Adafruit_CharLCDPlate.GREEN)
			lcd.message("SUCCESS!\nBadge Scanned")							
			sleep(2)									
			
			if department == "45" or department == "46" or department == "47": 
			# This is a maintenance employee				
				conn = pyodbc.connect("DSN=WAGODB;UID=sa;PWD=moldex")
				cursor = conn.execute("select state from machinestate where machineid = ?", machineid)
				row = cursor.fetchone()
				conn.close()
				state = row[0]					
				
				if state == 0:
					print "Starting Maintenance"
					isUnderMaintenance = True
					conn = pyodbc.connect("DSN=WAGODB;UID=sa;PWD=moldex")
					cursor = conn.execute("{call dbo.MaintenanceStart(?, ?)}", machineid, dt.datetime.now())	
					conn.commit()	
					conn.close()																										
					# TODO: Dispatch async handler to flash led screen
							
					
				if state == 1:
					print "Ending Maintenance"
					isUnderMaintenance = False
					conn = pyodbc.connect("DSN=WAGODB;UID=sa;PWD=moldex")
					cursor = conn.execute("{call dbo.MaintenanceEnd(?, ?)}", machineid, dt.datetime.now())	
					conn.commit()
					conn.close()										
					# TODO: Dispatch async handler to stop flashing led screen
					
						
					
			else: 
				# This is NOT a maintenance employee
				conn = pyodbc.connect("DSN=WAGODB;UID=sa;PWD=moldex")
				cursor = conn.execute("{call dbo.EmployeeScan(?, ?, ?)}", machineid, barcode, dt.datetime.now())
				conn.commit()
				conn.close()
				lcd.clear()
				lcd.backlight(Adafruit_CharLCDPlate.GREEN)
				lcd.message("SUCCESS!\nBadge Scanned")							
				sleep(2)
				lcd.backlight(Adafruit_CharLCDPlate.TEAL)
			
	except Exception as e:
		errorHandler(e)
		pass
	

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
		
def ONT(channel):
	global isUnderMaintenance
	print "\nOperator Notices Trouble"
	conn = pyodbc.connect("DSN=WAGODB;UID=sa;PWD=moldex")
	cursor = conn.execute("{call dbo.ONT(?, ?)}", machineid, dt.datetime.now())
	conn.commit()
	conn.close()
	
	# TODO: Need the same threading here as well for all UI updating...
	while 
		lcd.clear()
		lcd.backlight(Adafruit_CharLCDPlate.RED)
		lcd.message("   Maintenance\n     Needed")
		sleep(1)
		lcd.clear()
		lcd.backlight(Adafruit_CharLCDPlate.ON)
		sleep(1)
		

	
	
def mainloop():
	while True:
		try:
			CheckMachineState()
			barcode = raw_input("Please Scan A Barcode:")
			actonbarcode(barcode)
		except Exception as e:
			errorHandler(e)
			pass		
			


GPIO.setmode(GPIO.BOARD)
GPIO.setup(ontSwitch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # ONT Switch
GPIO.add_event_detect(ontSwitch, GPIO.RISING, callback=ONT, bouncetime=300)




