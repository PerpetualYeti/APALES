#!/usr/bin/python
"""
Simple g-code streaming script
"""
 
import serial
import time
import argparse
import os

def send_wake_up(ser):
    # Wake up
    # Hit enter a few times to wake the Printrbot
    #ser.write(str.encode("\r\n\r\n"))
    time.sleep(0.5)   #    Wait for Printrbot to initialize
    ser.flushInput()  # Flush startup text in serial input

GRBL_port_path = 'COM6'
gcode_path = os.path.join('gcode_examples', 'output.nc')
 
## show values ##
print(f'USB Port:  {GRBL_port_path}' )
print (f'Gcode file: {gcode_path}')


def removeComment(string):
	if (string.find(';')==-1):
		return string
	else:
		return string[:string.index(';')]
 
# Open serial port
#s = serial.Serial('/dev/ttyACM0',115200)
try:
	s = serial.Serial(GRBL_port_path,115200)
	print ('Opening Serial Port')
except:
	print("COM PORT NOT FOUND")
	exit()
 
# Open g-code file
#f = open('/media/UNTITLED/shoulder.g','r');
f = open(gcode_path,'r')
print ('Opening gcode file')
 
send_wake_up(s)
print ('Sending gcode')
 
# Stream g-code
for line in f:
	l = removeComment(line)
	l = l.strip() # Strip all EOL characters for streaming
	if  (l.isspace()==False and len(l)>0) :
		print ('Sending: ' + l)
		command = str.encode(l + '\n')
		s.write(command) # Send g-code block
		grbl_out = s.readline() # Wait for response with carriage return
		print (f' :  {grbl_out.strip()}')
 
# Wait here until printing is finished to close serial port and file.
input("  Press <Enter> to exit.")
 
# Close file and serial port
f.close()
s.close()

