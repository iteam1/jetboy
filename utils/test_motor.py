'''
Author: locchuong
Updated: 30/8/22
Description:
	test motor controller
'''

import serial
from serial.tools import list_ports
import time

# list all serial ports
ports = list_ports.comports()
for port,desc,hwid in sorted(ports):
	print("{}: {} [{}]".format(port,desc,hwid))

# choice your port
port  = input('Enter your port name: ')
device = serial.Serial(port,baudrate = 9600,timeout = 0.1)

if __name__ == "__main__":
	while True:
		x = input('Enter the string: ')
		# x == exit then exit
		if x == "exit":
			break
		x = x + "q" # use a character you can see to recognize a frame
		print(f'sending string: {x}')
		#arduino.write(bytes(x,'utf-8'))
		device.write(x.encode())
	# exit
	print("exiting...")
	exit()