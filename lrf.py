#!/usr/bin/env python
from time import sleep

def main():
	while True:
		line = raw_input("Please enter a 1 or 0:")		
		longrunningfunction(int(line))

def longrunningfunction(invar):
	# if invar == 1 then do LRO (long running operation)
	while invar == 1:
		print "Ok I am a long running function"
		sleep(3)
	# if invar == 0 then return to caller
	return
	
main()
	
# please illustrate how I can take more input and then stop the longrunningfunction
# the idea is that while a machine is "under maintenance" that a message must flash
# on the LED screen, for an indeterminate amount of time. i.e. until the mechanic
# is finished with the job.
#
# I realize that you may not be able to toggle it by calling the function again,
# as in this test case, you never get an option to call it again because the function
# is tying up the calling thread
#
# we discussed breifly that threads may not be necessary, I have looked into signals
# and threadpooling, but I remember you said you have a few ideas on how to do this.
#
# before, i was setting a global variable to true and then having a thread loop until
# the global var went false. The problem as presented is that the thread, once it is
# done with its job, cant be called again to start.
#
# basically need a solution to dispatch LED screen updates while allowing the main
# thread to continue its execution, taking more input.
#
# thanks a bunch! - Steve
