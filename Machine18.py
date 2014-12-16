from threading import Thread
from time import sleep
import RPi.GPIO as GPIO
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
import datetime
import pyodbc
import socket



lcd = Adafruit_CharLCDPlate()
lcd.backlight(Adafruit_CharLCDPlate.TEAL)

isUnderMaintenance = False
needsMaintenance = False

machineid = socket.gethostname()

def CheckMachineState():
	conn = pyodbc.connect("DRIVER={ms-sql};SERVER=moldex-sl.moldex.com;PORT=1433;DATABASE=wagodb;UID=sa;PWD=moldex")
	cursor = conn.execute("select sku, lotnumber from machinestate where machineid = ?", machineid)
	
	row = cursor.fetchone()
	sku = row[0]
	lot = row[1]
	conn.close()

	lcd.clear()
	lcd.backlight(Adafruit_CharLCDPlate.TEAL)
	lcd.message("SKU: " + sku + "\nLot: " + lot)
	
def LogError(errMessage):
	conn = pyodbc.connect("DRIVER={ms-sql};SERVER=moldex-sl.moldex.com;PORT=1433;DATABASE=wagodb;UID=sa;PWD=moldex")
	cursor = conn.execute("{call dbo.LogError(?, ?)}", machineid, str(errMessage))
	conn.commit()
	conn.close()

def ONT(channel):
	global main_loop
	global isUnderMaintenance
	global needsMaintenance	
	conn = pyodbc.connect("DRIVER={ms-sql};SERVER=moldex-sl.moldex.com;PORT=1433;DATABASE=wagodb;UID=sa;PWD=moldex")
	cursor = conn.execute("{call dbo.ONT(?, ?)}", machineid, datetime.datetime.now())
	conn.commit()
	conn.close()
	isUnderMaintenance = False
	needsMaintenance = True
	main_loop.start_service_thread()
	
	

def MaintenanceNeededMsg():
	lcd.clear()
	lcd.backlight(Adafruit_CharLCDPlate.RED)
	lcd.message("   Maintenance\n     Needed")
	sleep(1)
	lcd.clear()
	lcd.backlight(Adafruit_CharLCDPlate.ON)
	sleep(1)
	lcd.message("   Maintenance\n     Needed")
	
def UnderMaintenanceMessage():
	lcd.clear()
	lcd.backlight(Adafruit_CharLCDPlate.RED)
	lcd.message("  Maintenance\n      Mode")
	sleep(5)
	lcd.clear()
	lcd.backlight(Adafruit_CharLCDPlate.RED)
	lcd.message("     UNDER \n  MAINTENANCE")
	sleep(3)
	CheckMachineState()
	sleep(3)

def ErrorRoutine():
	lcd.clear()
	lcd.backlight(0x01)
	lcd.message("     ERROR")
	sleep(.5)
	lcd.clear()
	lcd.message("\n     ERROR")
	sleep(.5)
	lcd.clear()
	lcd.message("     ERROR")		
	sleep(.5)
	lcd.clear()
	lcd.message("\n     ERROR")
	sleep(.5)
	lcd.clear()
	lcd.message("     ERROR")
	sleep(.5)
	lcd.clear()
	lcd.message("\n     ERROR")
	sleep(.5)
	lcd.clear()
	lcd.message("     ERROR")		
	sleep(.5)
	lcd.clear()
	lcd.message("\n     ERROR")
	sleep(.5)
	lcd.clear()
	lcd.backlight(Adafruit_CharLCDPlate.TEAL)
	


def WhatWasScanned(barcode):
	try:
	   	global isUnderMaintenance
	   	global needsMaintenance
		global main_loop		
		
		if len(barcode) == 7:
			lcd.clear()
			lcd.message("SKU:\n" + barcode)
			sleep(3)
			conn = pyodbc.connect("DRIVER={ms-sql};SERVER=moldex-sl.moldex.com;PORT=1433;DATABASE=wagodb;UID=sa;PWD=moldex")
			cursor = conn.execute("{call dbo.SKU(? , ?)}", machineid, barcode )
			conn.commit()
			lcd.clear()
			lcd.backlight(Adafruit_CharLCDPlate.GREEN)
			lcd.message("SUCCESS!\nSKU Updated")			
			conn.close()
			sleep(2)
			lcd.backlight(Adafruit_CharLCDPlate.TEAL)
	
		if len(barcode) == 13:
			lcd.clear()
			lcd.message("Lot Roll Number:\n" + barcode)
			sleep(3)
			conn = pyodbc.connect("DRIVER={ms-sql};SERVER=moldex-sl.moldex.com;PORT=1433;DATABASE=wagodb;UID=sa;PWD=moldex")
			cursor = conn.execute("{call dbo.LotScan(?, ?, ?)}", machineid, barcode, datetime.datetime.now())
			conn.commit()
			lcd.clear()
			lcd.backlight(Adafruit_CharLCDPlate.GREEN)
			lcd.message("SUCCESS!\nLot Updated")			
			conn.close()
			sleep(2)
			lcd.backlight(Adafruit_CharLCDPlate.TEAL)
		
		if len(barcode) == 6:
			lcd.clear()
			lcd.message("Badge ID:\n" + barcode)
			sleep(3)
			listBadge = list(barcode)			
			while listBadge[0] == '0':
				listBadge.remove(listBadge[0])
			barcode = "".join(listBadge)
			conn = pyodbc.connect("DRIVER={ms-sql};SERVER=moldex-sl.moldex.com;PORT=1433;DATABASE=NOVA3000_MOLDEX_METRIC;UID=sa;PWD=moldex")
			cursor = conn.execute("select cfirstname, clastname, cgroup2 from employee where ncardnum = ?", barcode)	
			row = cursor.fetchone()
			firstname = row[0]	
			lastname = row[1]
			department = row[2]
			department = department.rstrip()
			department = department.lstrip()			
			conn.close()									
			if department == "45" or department == "46" or department == "47": # This is a maintenance employee				
				conn = pyodbc.connect("DRIVER={ms-sql};SERVER=moldex-sl.moldex.com;PORT=1433;DATABASE=wagodb;UID=sa;PWD=moldex")
				cursor = conn.execute("select state from machinestate where machineid = ?", machineid)
				row = cursor.fetchone()
				state = row[0]	
						
				
				if state == 0:
					print "Starting Maintenance"
					conn = pyodbc.connect("DRIVER={ms-sql};SERVER=moldex-sl.moldex.com;PORT=1433;DATABASE=wagodb;UID=sa;PWD=moldex")
					cursor = conn.execute("{call dbo.MaintenanceStart(?, ?)}", machineid, datetime.datetime.now())	
					conn.commit()							
					isUnderMaintenance = True
					needsMaintenance = False
					main_loop.start_service_thread()
					return
					
											
				if state == 1:
					print "Ending Maintenance"
					conn = pyodbc.connect("DRIVER={ms-sql};SERVER=moldex-sl.moldex.com;PORT=1433;DATABASE=wagodb;UID=sa;PWD=moldex")
					cursor = conn.execute("{call dbo.MaintenanceEnd(?, ?)}", machineid, datetime.datetime.now())	
					conn.commit()
					isUnderMaintenance = False
					main_loop.stop_service_thread()
					return
					
			else: # This is NOT a maintenance employee
				conn = pyodbc.connect("DRIVER={ms-sql};SERVER=moldex-sl.moldex.com;PORT=1433;DATABASE=wagodb;UID=sa;PWD=moldex")
				cursor = conn.execute("{call dbo.EmployeeScan(?, ?)}", machineid, barcode)
				conn.commit()
				lcd.clear()
				lcd.backlight(Adafruit_CharLCDPlate.GREEN)
				lcd.message("SUCCESS!\nBadge Scanned")							
				sleep(2)
				lcd.backlight(Adafruit_CharLCDPlate.TEAL)
			
			# Clean up				
			conn.close()
			lcd.clear()
			lcd.backlight(Adafruit_CharLCDPlate.TEAL)
			lcd.message(firstname + "\n" + lastname)
			sleep(5)
	except Exception as e:	
		LogError(e)	
		ErrorRoutine()


class BaseThread(Thread):
    def __init__(self, parent=None):
        super(BaseThread, self).__init__()
        self.parent = parent
        self.stay_alive = True

    def run(self):
        pass

    def interruptible_sleep(self):
        '''Sleep conditionally, until stay_alive is False'''
        while self.stay_alive:
            sleep(0.1)

    def halt(self):
        self.stay_alive = False


class MainLoopThread(BaseThread):
    def __init__(self):
        super(MainLoopThread, self).__init__()
        self.barcode_thread = None
        self.service_thread = None

    def start_barcode_thread(self):
        self.stop_barcode_thread()
        self.barcode_thread = BarcodeThread()
        self.barcode_thread.start()

    def stop_barcode_thread(self):
        if self.barcode_thread is not None:
            try:
                self.barcode_thread.halt()
                self.barcode_thread.join()
            except:
                pass

    def start_service_thread(self):
        self.stop_service_thread()
        self.service_thread = ServiceThread()
        self.service_thread.start()

    def stop_service_thread(self):
        if self.service_thread is not None:
            try:
                self.service_thread.halt()
                self.service_thread.join()
            except:
                pass


main_loop = MainLoopThread()


class ServiceThread(BaseThread):
    def run(self):
        global isUnderMaintenance
        global needsMaintenance
       
        while isUnderMaintenance == True:
			UnderMaintenanceMessage()
            				
                        
        while needsMaintenance == True:
			MaintenanceNeededMsg()

        self.interruptible_sleep()  # Sleep until thread halt


class BarcodeThread(BaseThread):
    def run(self):
        global isUnderMaintenance
        global needsMaintenance
        global main_loop
        ontSwitch = 11
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(ontSwitch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(ontSwitch, GPIO.RISING, callback=ONT, bouncetime=300)
               
        
        CheckMachineState()

        while True:
            barcode = raw_input("Please Scan A Barcode: ")
            WhatWasScanned(barcode)
            
            CheckMachineState()
            
            
            #if barcode == str(True):
            #    isUnderMaintenance = True
            #    print str(isUnderMaintenance)
            #    print "Starting Service Thread"
            #    main_loop.start_service_thread()
            #else:
            #    isUnderMaintenance = False
            #    print str(isUnderMaintenance)
            #    print "Stopping Service Thread"
            #    main_loop.stop_service_thread()

        #self.interruptible_sleep()  # Sleep until thread halt, useful if needed


# Usage example:



def main():
    global main_loop
    main_loop.start_barcode_thread()
    main_loop.interruptible_sleep()
    #main_loop.start_service_thread()
    # main_loop.interruptible_sleep()
    # from other code, you can call the following methods to control the main loop - remember main_loop must be a global
    # main_loop.start_barcode_thread()
    # main_loop.stop_barcode_thread()
    # main_loop.start_service_thread()
    # main_loop.stop_service_thread()

if __name__ == "__main__":
    main()

