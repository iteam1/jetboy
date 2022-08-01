'''
Author: locchuong
Updated: 1/8/22
Description:
	test serial communicate with arduino
'''

import serial
from serial.tools import list_ports
import time 

ports = list_ports.comports()
for port,desc,hwid in sorted(ports):
	print("{}: {} [{}]".format(port,desc,hwid))

port  = input('Enter your port name: ')
arduino = serial.Serial(port,baudrate = 9600,timeout = 0.1)

if __name__ == "__main__":
	while True:
		x = input('Enter the framework: ')
		x = x + "a" # use a character you can see to recognize a frame
		print(x)
		#arduino.write(bytes(x,'utf-8'))
		arduino.write(x.encode())