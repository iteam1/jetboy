'''
Author: locchuong
Updated: 7/9/22
Description:
	This python program control the GPIO of Jetson-Nano board, it read the command from the database and execute it.
	Run this program at the begining.
	If you import class controller from ./Jetson-Nano the GPIO_controller will run from the top to the end of the class controlle
	meaning it will create the connection and the cursor to the database and input this to class controller

	id c.fetchone()[0]
	name c.fetchone()[1]
	command c.fetchone()[2]
	content c.fetchone()[3]
	emotion c.fetchone()[4]
	image c.fetchone()[5]
	itype c.fetchone()[6]
	estop c.fetchone()[7]
	obs_f c.fetchone()[8]
	obs_b c.fetchone()[9]
	obs_l c.fetchone()[10]
	obs_r c.fetchone()[11]
'''

# Import the the required libraries
import RPi.GPIO
import sqlite3 
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

prev_emotion = emotion = "sleep"

# Create the connection to the database and the cursor
conn = sqlite3.connect("./robot/site.db") # ./Jetson-Nano you must define this conn before add in into default keyword arg 
c = conn.cursor()  # you must define this c before add in into default keyword arg 

class controller():
	def __init__(self,ML_DIR_pin = ML_DIR_pin,ML_RUN_pin = ML_RUN_pin,MR_DIR_pin = MR_DIR_pin,MR_RUN_pin = MR_RUN_pin,
					OBS_F_pin = OBS_F_pin,OBS_B_pin = OBS_B_pin,OBS_L_pin = OBS_L_pin,OBS_R_pin = OBS_R_pin,GPIO = RPi.GPIO,
						conn = conn):

		# Serial port
		self.arm_port = None
		self.arm = None # serial device object
		self.emoled_port = None
		self.emoled = None # serial device object
		self.no_port = 0
		
		self.ML_DIR_pin = ML_DIR_pin # driver left dir pin
		self.ML_RUN_pin = ML_RUN_pin # driver left run pin
		self.MR_DIR_pin = MR_DIR_pin # driver right dir pin
		self.MR_RUN_pin = MR_RUN_pin # driver right run pin

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
		self.conn = conn 
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
		# update all signals for the controller before you run
		#self.update_input()
		# print(self.ESTOP)
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
		# update all signals for the controller before you run
		#self.update_input()
		# print(self.ESTOP)
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
		# update all signals for the controller before you run
		#self.update_input()
		# print(self.ESTOP)
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
		# update all signals for the controller before you run
		#self.update_input()
		# print(self.ESTOP)
		if not self.ESTOP:
			self.GPIO.output(self.MR_DIR_pin,0)
			self.GPIO.output(self.ML_DIR_pin,1)
			self.GPIO.output(self.MR_RUN_pin,1)
			self.GPIO.output(self.ML_RUN_pin,1)
		else:
			print('Emergency stop activated! this command can not execute')

	def db_stop_update(self):
		'''
		Use this function to set the command in database to stop after bit moving
		'''
		c = self.conn.cursor()
		c.execute("""
			UPDATE robot
			SET command = "stop"
			WHERE id = 1
			""")
		self.conn.commit()
		#self.conn.close()

	def bit_forward(self,delay):
		'''
		Motors move abit forward
		'''
		self.forward()
		time.sleep(delay)
		self.stop()
		self.db_stop_update()

	def bit_backward(self,delay):
		'''
		Motors move abit backward
		'''
		self.backward()
		time.sleep(delay)
		self.stop()
		self.db_stop_update()

	def bit_turnleft(self,delay):
		'''
		Motors turn left abit
		'''
		self.turnleft()
		time.sleep(delay)
		self.stop()
		self.db_stop_update()

	def bit_turnright(self,delay):
		'''
		Motor turn right abit
		'''
		self.turnright()
		time.sleep(delay)
		self.stop()
		self.db_stop_update()

	def update_input(self):
		'''
		Use this function to read ESTOP value in database and read sensor values and update it into robot's database
			conn: the connection to database
			c: cusor of the connection to database
		'''

		# Fetch all value columns in database
		c = self.conn.cursor()
		c.execute("""
			SELECT *FROM robot WHERE id = 1
			""")

		data = c.fetchone() # Get all row
		self.conn.commit()
		# self.conn.close()
		# Read ESTOP from the server ,write it out to database and storage it into robot object
		self.ESTOP = data[7] # read emergency stop

		# Read ultrasonic sensor signal save it to database
		self.OBS_F_value = self.GPIO.input(self.OBS_F_pin) # read front obstacle value
		self.OBS_B_value = self.GPIO.input(self.OBS_B_pin) # read back obstacle value
		self.OBS_L_value = self.GPIO.input(self.OBS_L_pin) # read left obstacle value
		self.OBS_R_value = self.GPIO.input(self.OBS_R_pin) # read right obstacle value

		# c.execute("""
		# 	INSERT INTO robot(obs_f,obs_b,obs_l,obs_r) VALUES(?,?,?,?)
		# 	""",(self.OBS_F_value,self.OBS_B_value,self.OBS_L_value,self.OBS_B_value))

		# Update the values of sensor into database
		c.execute("""
			UPDATE robot
			SET obs_f = ?,
				obs_b = ?,
				obs_l = ?,
				obs_r = ?
			WHERE id = 1
			""",(self.OBS_F_value,self.OBS_B_value,self.OBS_L_value,self.OBS_R_value))
		self.conn.commit()

	def read_estop(self):
		'''
		This function read the estop value in the database and return it
		'''
		c = self.conn.cursor()
		c.execute("""
			SELECT *FROM robot WHERE id = 1
			""")

		data = self.c.fetchone() # Get all row
		self.conn.commit()
		# self.conn.close()

		# Read ESTOP from the server 
		estop = data[7] # read emergency stop

		return estop

	def read_obstacles(self):
		'''
		This function read the estop value in the database and return it
		'''

		c = self.conn.cursor()

		c.execute("""
			SELECT *FROM robot WHERE id = 1
			""")

		data = c.fetchone() # Get all row
		self.conn.commit()
		# self.conn.close()

		# Read ESTOP from the server 
		obs_f = data[8] # read front ultrasonics sensors
		obs_b = data[9] # read back ultrasonics sensors
		obs_l = data[10] # read left ultrasonics sensors
		obs_r = data[11] # read right ultrasonics sensors

		return obs_f,obs_b,obs_l,obs_r

	def read_command(self):
		'''
		This function read the command value in database and return it
		'''
		c = self.conn.cursor()
		c.execute(f"SELECT *FROM robot WHERE id = 1")
		data = c.fetchone()
		command = data[2]
		self.conn.commit()
		# self.conn.close()
		return command

	def read_emotion(self):
		'''
		This function read the command value in database and return it
		'''
		c = self.conn.cursor()
		c.execute(f"SELECT *FROM robot WHERE id = 1")
		data = c.fetchone()
		emotion = data[4]
		itype = data[6]
		self.conn.commit()
		return emotion,itype

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
	
	print("Robot GPIO controller is running...")

	while True:

		# **********************[CONTROL EMOLED]**********************
		# Read the emotion
		emotion,itype = controller.read_emotion()
		if itype == "emo":
			if prev_emotion !=emotion:
				prev_emotion = emotion
				emotion =emotion+'q'
				#print(f"emotion: {emotion}")
				controller.emoled.write(emotion.encode())

		# Read the command
		command = controller.read_command()

		# Read the inputs and write it into the database
		controller.update_input()
		#print(controller.ESTOP,controller.OBS_F_value,controller.OBS_B_value,controller.OBS_L_value,controller.OBS_R_value)

		#Write the output
		if command == "kill":
			print("Stop motor & Clean up")
			# reset kill command for the next start
			controller.db_stop_update()
			print('database cleaned up command!')
			break

		# **********************[CONTROL MOTOR]**********************
		# continously moving 
		elif command == "stop":
			controller.stop()

		elif command == "forward":
			controller.forward()

		elif command == "backward":
			controller.backward()

		elif command == "turnleft":
			controller.turnleft()

		elif command == "turnright":
			controller.turnright()
			
		# moving a bit and stop meaning we have to reset 
		elif command == "bit_forward":
			controller.bit_forward(0.3)

		elif command == "bit_backward":
			controller.bit_backward(0.3)

		elif command == "bit_turnleft":
			controller.bit_turnleft(0.2)

		elif command == "bit_turnright":
			controller.bit_turnright(0.2)

		# **********************[CONTROL ARM]**********************

		elif command == "peeps":
			command = command + "q"
			controller.arm.write(command.encode())
			controller.db_stop_update()

		elif command == "grip":
			if not controller.ESTOP:
				command = command + "q"
				controller.arm.write(command.encode())
			else:
				print("Robot's Arm blocked [EMERGENCY STOP]")
			controller.db_stop_update() # stop after sending command or estop activate

		elif command == "step":
			if not controller.ESTOP:
				command = command + "q"
				controller.arm.write(command.encode())
			else:
				print("Robot's Arm blocked [EMERGENCY STOP]")
			controller.db_stop_update()

		elif command == "forward":
			if not controller.ESTOP:
				command = command + "q"
				controller.arm.write(command.encode())
			else:
				print("Robot's Arm blocked [EMERGENCY STOP]")
			controller.db_stop_update()

		elif command == "backward":
			if not controller.ESTOP:
				command = command + "q"
				controller.arm.write(command.encode())
			else:
				print("Robot's Arm blocked [EMERGENCY STOP]")
			controller.db_stop_update()

		elif command == "up":
			if not controller.ESTOP:
				command = command + "q"
				controller.arm.write(command.encode())
			else:
				print("Robot's Arm blocked [EMERGENCY STOP]")
			controller.db_stop_update()

		elif command == "down":
			if not controller.ESTOP:
				command = command + "q"
				controller.arm.write(command.encode())
			else:
				print("Robot's Arm blocked [EMERGENCY STOP]")
			controller.db_stop_update()

		elif command == "hello":
			if not controller.ESTOP:
				command = command + "q"
				controller.arm.write(command.encode())
			else:
				print("Robot's Arm blocked [EMERGENCY STOP]")
			controller.db_stop_update()

		else:
			print("Command does not exist!")
			pass

		time.sleep(0.1) # if you don't delay, the while loop run so fast and it will crack the other propgram has queries to the database

	# if you out the while loop
	controller.stop()

	controller.GPIO.cleanup()
	#RPi.GPIO.cleanup()
	
	conn.close()
	
	print("Exit robot GPIO controller...")

	exit()