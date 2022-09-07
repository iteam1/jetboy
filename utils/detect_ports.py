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
		self.arm_port = None
		self.emoled_port = None
		self.no_port = 0

if __name__ =="__main__":

	# init myports
	myports = myports()

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
		# print("sended identify command to port: {}".format(port))
		data = device.readline()
		device_name = data.decode().strip()
		# print("data: {}".format(data.decode()))
		print("port: {} is {}".format(port,device_name))

		if device_name == "arm":
			myports.arm_port = port 
		elif device_name == "emoled":
			myports.emoled_port == port
		else:
			print("port: {} - {} is not identified".format(port,device_name))
