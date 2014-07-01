from threading import Thread
from time import sleep



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


class BarcodeThread(BaseThread):

    def run(self):
		while True:
			try:
				#CheckMachineState()
				barcode = raw_input("This is from Fernando's Code:")
				#actonbarcode(barcode)
			except Exception as e:
				print "Something messed up"
				#errorHandler(e)
		#self.interruptible_sleep()  
        # add your barcode scanning code here
        # The following calls can be made to control the state of threads from here
        # self.parent.start_barcode_thread()
        # self.parent.stop_barcode_thread()
        # self.parent.start_service_thread()
        # self.parent.stop_service_thread()
        
        


class ServiceThread(BaseThread):

    def run(self):
        # add your service mode handling code here
        # The following calls can be made to control the state of threads from here
        # self.parent.start_barcode_thread()
        # self.parent.stop_barcode_thread()
        # self.parent.start_service_thread()
        # self.parent.stop_service_thread()
        self.interruptible_sleep()  # Sleep until thread halt


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
        self.stop_barcode_thread()
        self.service_thread = ServiceThread()
        self.service_thread.start()

    def stop_service_thread(self):
        if self.service_thread is not None:
            try:
                self.service_thread.halt()
                self.service_thread.join()
            except:
                pass


# Usage example:
main_loop = MainLoopThread()


def main():
    global main_loop
    main_loop.start_barcode_thread()
    main_loop.interruptible_sleep()
    # from other code, you can call the following methods to control the main loop - remember main_loop must be a global
    # main_loop.start_barcode_thread()
    # main_loop.stop_barcode_thread()
    # main_loop.start_service_thread()
    # main_loop.stop_service_thread()
    
main()
