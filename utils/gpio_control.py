'''
Author: locchuong
Updated: 7/9/22
Description:
	test motor controller and robot arm via command
'''

# Import the the required libraries
import RPi.GPIO
import time
import serial
from serial.tools import list_ports

# Define pin number
# OUTPUT pins name
ML_DIR_pin = 24 # motor left direction
ML_RUN_pin = 23 # motor left run
MR_DIR_pin = 22 # motor right direction
MR_RUN_pin = 21 # motor right run
# INPUT pins name
OBS_F_pin = 15 # front ultrasonic sensor
OBS_B_pin = 16 # back ultrasonic sensor 
OBS_L_pin = 18 # left ultrasonic sensor 
OBS_R_pin = 19 # right ultrasonic sensor

get_id = "whoq" # get name of serial device

# gpio controller but no connect to database
class controller():
	def __init__(self,ML_DIR_pin = ML_DIR_pin,ML_RUN_pin = ML_RUN_pin,MR_DIR_pin = MR_DIR_pin,MR_RUN_pin = MR_RUN_pin,
					OBS_F_pin = OBS_F_pin,OBS_B_pin = OBS_B_pin,OBS_L_pin = OBS_L_pin,OBS_R_pin = OBS_R_pin,GPIO = RPi.GPIO):
		
		# Serial port
		self.arm_port = None
		self.arm = None
		self.emoled_port = None
		self.emoled = None
		self.no_port = 0

		# Define gpio pins for motor controller
		self.ML_DIR_pin = ML_DIR_pin # driver left dir pin
		self.ML_RUN_pin = ML_RUN_pin # driver left run pin
		self.MR_DIR_pin = MR_DIR_pin # driver right dir pin
		self.MR_RUN_pin = MR_RUN_pin # driver right run pin

		# Define gpio pins for obstacle sensors
		self.OBS_F_pin = OBS_F_pin # front obstacle pin
		self.OBS_F_value = 0 # front obstacle value
		self.OBS_B_pin = OBS_B_pin # back obstacle pin
		self.OBS_B_value = 0 # back obstacle value  
		self.OBS_L_pin = OBS_L_pin # left obstacle pin
		self.OBS_L_value = 0 # left obstacle value
		self.OBS_R_pin = OBS_R_pin # right obstacle pin
		self.OBS_R_value = 0 # right obstacle value

		self.ESTOP = 0 # estop value 0 = O.K, 1 = STOP NOW
		self.GPIO = GPIO

		#initialize gpio
		self.GPIO.setmode(GPIO.BOARD) # Set the pin's definition mode

		# Define I/O for motor control pins
		self.GPIO.setup(self.ML_DIR_pin,self.GPIO.OUT)
		self.GPIO.setup(self.ML_RUN_pin,self.GPIO.OUT)
		self.GPIO.setup(self.MR_DIR_pin,self.GPIO.OUT)
		self.GPIO.setup(self.MR_RUN_pin,self.GPIO.OUT)
		
		# Define I/O for sensor control pins
		self.GPIO.setup(self.OBS_F_pin,self.GPIO.IN)
		self.GPIO.setup(self.OBS_B_pin,self.GPIO.IN)
		self.GPIO.setup(self.OBS_L_pin,self.GPIO.IN)
		self.GPIO.setup(self.OBS_R_pin,self.GPIO.IN)

		# block motors run by EN pins
		self.GPIO.output(self.MR_RUN_pin,0)
		self.GPIO.output(self.ML_RUN_pin,0)
		self.GPIO.output(self.MR_DIR_pin,0)
		self.GPIO.output(self.ML_DIR_pin,0)

		# set database connection and cursor
		# self.conn = conn 
		#self.c = c 

	def stop(self):
		'''
		Stop motor immediately
		'''
		self.GPIO.output(self.MR_RUN_pin,0)
		self.GPIO.output(self.ML_RUN_pin,0)

	def forward(self):
		'''
		Motor run forward continously
		'''
		self.stop()
		if not self.ESTOP:
			self.GPIO.output(self.MR_DIR_pin,1)
			self.GPIO.output(self.ML_DIR_pin,1)
			self.GPIO.output(self.MR_RUN_pin,1)
			self.GPIO.output(self.ML_RUN_pin,1)			
		else:
			print('Emergency stop activated! this command can not execute')

	def backward(self):
		'''
		Motor run backward continously
		'''
		self.stop()
		if not self.ESTOP:
			self.GPIO.output(self.MR_DIR_pin,0)
			self.GPIO.output(self.ML_DIR_pin,0)
			self.GPIO.output(self.MR_RUN_pin,1)
			self.GPIO.output(self.ML_RUN_pin,1)			
		else:
			print('Emergency stop activated! this command can not execute')

	def turnleft(self):
		'''
		Motor turn left continously
		'''
		self.stop()
		if not self.ESTOP:
			self.GPIO.output(self.MR_DIR_pin,1)
			self.GPIO.output(self.ML_DIR_pin,0)
			self.GPIO.output(self.MR_RUN_pin,1)
			self.GPIO.output(self.ML_RUN_pin,1)
		else:
			print('Emergency stop activated! this command can not execute')

	def turnright(self):
		'''
		Motor turn right continously
		'''
		self.stop()
		if not self.ESTOP:
			self.GPIO.output(self.MR_DIR_pin,0)
			self.GPIO.output(self.ML_DIR_pin,1)
			self.GPIO.output(self.MR_RUN_pin,1)
			self.GPIO.output(self.ML_RUN_pin,1)
		else:
			print('Emergency stop activated! this command can not execute')

	def bit_forward(self,delay):
		'''
		Motors move abit forward
		'''
		self.forward()
		time.sleep(delay)
		self.stop()

	def bit_backward(self,delay):
		'''
		Motors move abit backward
		'''
		self.backward()
		time.sleep(delay)
		self.stop()

	def bit_turnleft(self,delay):
		'''
		Motors turn left abit
		'''
		self.turnleft()
		time.sleep(delay)
		self.stop()

	def bit_turnright(self,delay):
		'''
		Motor turn right abit
		'''
		self.turnright()
		time.sleep(delay)
		self.stop()

	def read_sensors(self):
		'''
		Use to read sensors signal
		'''

		# Read ultrasonic sensor signal save it to database
		self.OBS_F_value = self.GPIO.input(self.OBS_F_pin) # read front obstacle value
		self.OBS_B_value = self.GPIO.input(self.OBS_B_pin) # read back obstacle value
		self.OBS_L_value = self.GPIO.input(self.OBS_L_pin) # read left obstacle value
		self.OBS_R_value = self.GPIO.input(self.OBS_R_pin) # read right obstacle value

if __name__ == "__main__":

	# init controller
	controller = controller()
	controller.stop()

	# list all port
	print("Checking serial port...")
	port_list = []
	desc_list = []
	hwid_list = []
	ports = list_ports.comports()
	controller.no_port = len(ports)
	print("Number of serial ports {}".format(controller.no_port))

	for port,desc,hwid in sorted(ports):
		port_list.append(port)
		desc_list.append(desc)
		hwid_list.append(hwid)
		print("{} - {} - {}".format(port,desc,hwid))

	for port in port_list:
		device = serial.Serial(port,baudrate=9600,timeout=0.1)
		device.write(get_id.encode())
		# print("sended identify command to port: {}".format(port))
		data = device.readline()
		device_name = data.decode().strip()
		# print("data: {}".format(data.decode()))
		print("port: {} is {}".format(port,device_name))

		if device_name == "arm":
			controller.arm_port = port
			controller.arm = device
		elif device_name == "emoled":
			controller.emoled_port == port
			controller.emoled = device
		else:
			print("port: {} - {} is not identified".format(port,device_name))

	while True:
	
		x = input('Enter the your moving command: ')
	
		# x == exit then exit
		if x == "exit":
			break

		elif x == "w":
			controller.forward()

		elif x == "ww":
			controller.bit_forward(delay = 0.1)

		elif x == "s":
			controller.backward()

		elif x == "ss":
			controller.bit_backward(delay = 0.1)

		elif x == "a":
			controller.turnleft()

		elif x == "aa":
			controller.bit_turnleft(delay = 0.1)

		elif x == "d":
			controller.turnright()

		elif x == "dd":
			controller.bit_turnright(delay = 0.1)

		elif x =="test":
			x = x + "q"
			controller.arm.write(x.encode())

		elif x =="smile":
			x = x + "q"
			controller.emoled.write(x.encode())

		elif x =="sad":
			x = x + "q"
			controller.emoled.write(x.encode())

		elif x =="angry":
			x = x + "q"
			controller.emoled.write(x.encode())

		elif x =="sleep":
			x = x + "q"
			controller.emoled.write(x.encode())

		elif x =="neutral":
			x = x + "q"
			controller.emoled.write(x.encode())

		elif x =="surprised":
			x = x + "q"
			controller.emoled.write(x.encode())

		elif x =="off":
			x = x + "q"
			controller.emoled.write(x.encode())

		else:
			controller.stop()

	# exit
	controller.GPIO.cleanup()
	print("exiting...")
	exit()