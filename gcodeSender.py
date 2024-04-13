# Senior Design 2 Spring 2024 Group 5: APALES
# Authors: Aly Megahed, Kavinaash Jesurajah, Nolan McGinley

""" 
Description: Python module to send gcode, either as a single line
or a whole (.nc) file. Uses pySerial interface to connect to Arduino
with GRBL 1.1 firmware. Contains instance methods to be imported into 
main file.
"""
 
import serial
import time
import os

class Sender:
	# Constructor to initialise serial connection parameters 
	def __init__(self, port: str, baudrate=115200):
		self.port = port
		self.baudrate = baudrate
		self.serial_connection = None
	
	# Begin serial connection
	def connect(self):
		try:
			self.serial_connection = serial.Serial(self.port, self.baudrate)
			print(f"Connected to serial port: {self.port}")
		except serial.SerialException as e:
			print(f"Connection failed. {e}")

	# End serial connection
	def disconnect(self):
		if self.serial_connection is not None:
			self.serial_connection.close()
			print(f"Disconnected from serial port: {self.port}")
	
	# Send single line g-code command
	def send_commmand(self, command : str) -> bool:
		if self.serial_connection is not None and self.serial_connection.is_open:
			try:
				self.serial_connection.write(command.encode('utf-8'))
			except Exception as e: 
				print(f"Command failed {e}")
				return False
		else:
			print("Serial connection is closed")
			return False
	
	# Send GRBL reset (Ctrl + X) and sleep for 0.5 seconds
	def send_wakeup(self) -> bool:
		if self.serial_connection is not None and self.serial_connection.is_open:
			try:
				print('Sending GRBL reset')
				self.serial_connection.write(b'\x18\x78')
				grbl_out = self.serial_connection.readline() # Wait for response with carriage return
				print (f' :  {grbl_out.strip()}')
				time.sleep(0.5)
				self.serial_connection.reset_input_buffer()
			except serial.SerialException as e:
				print(f"Connectioin failed {e}")
		else:
			print("Serial connection is closed")
			return False

	# Remove comments from g-code file
	def removeComment(string):
		if (string.find(';')==-1):
			return string
		else:
			return string[:string.index(';')]
	
	# Send complete g-code job
	def send_job(self) -> bool:
		# Open g-code file
		try:
			gcode_path = 'output.nc'
			f = open(gcode_path,'r')
		except FileNotFoundError as e:
			print(f"File not found {e}")

		if self.serial_connection is not None and self.serial_connection.is_open:
			try:
				print ('Sending gcode')
				# Stream g-code
				for line in f:
					l = Sender.removeComment(line)
					l = l.strip() # Strip all EOL characters for streaming
					if  (l.isspace()==False and len(l)>0) :
						print ('Sending: ' + l)
						command = str.encode(l + '\n')
						self.serial_connection.write(command) # Send g-code block
						grbl_out = self.serial_connection.readline() # Wait for response with carriage return
						print (f' :  {grbl_out.strip()}')

				# Wait here until printing is finished to close serial port and file.
				input("  Press <Enter> to exit.")
				f.close()
				self.disconnect()

			except Exception as e: 
				print(f"Error running job {e}")
				return False
		else:
			print("Serial connection is closed")
			return False
