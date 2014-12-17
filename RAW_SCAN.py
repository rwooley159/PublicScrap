#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2014 root <root@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import sys

fp = open('/dev/hidraw3', 'rb')
tStr = ''

while True:
	buffer = fp.read(8)
	
	for c in buffer:
		print "This is the value of c:\n"
		print str(ord(c))
		if ord(c) > 0:			
			tStr = tStr + c
			
	print "this is tStr"		
	print tStr + "\n"
	
	tStr = ""
	



def main():
	
	
	
	return 0

if __name__ == '__main__':
	main()

