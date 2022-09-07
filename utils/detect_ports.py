'''
Author: locchuong
Updated: 7/9/22
Description:
	identify multi serial port
'''
import serial
from serial.tools import list_ports

class myports():
	def __init__(self):
		arm_port = None
		emoled_port = None
		no_port = 0

if __name__ =="__main__":

	# list all port
	port_list = []
	desc_list = []
	hwid_list = []
	ports = list_ports.comports()

	for port,desc,hwid in sorted(ports):
		port_list.append(port)
		desc_list.append(desc)
		hwid_list.append(hwid)
		print("{}: {}: [{}]".format(port,desc,hwid))

	myports.no_port = len(ports)
	print("number of serial ports {}".format(myports.no_port))

	x = "whoq"
	for port in port_list:
		device = serial.Serial(port,baudrate=9600,timeout=0.1)
		device.write(x.encode())
		print("sended identify command to port: {}".format(port))
		data = device.readline()
		print("data: {}".format(data.decode()))

