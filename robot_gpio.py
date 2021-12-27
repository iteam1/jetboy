'''
Author: locchuong
Updated: 27/12/21
Description:
	This python program control the GPIO of Jetson-Nano board, it read the command from the database and execute it
	run this program at the begining.
	If you import class controller from ./Jetson-Nano the GPIO_controller will run from the top to the end of the class controlle
	meaning it will create the connection and the cursor to the database and input this to class controller

'''

import RPi.GPIO
import sqlite3 
import time

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

conn = sqlite3.connect("./robot/site.db") # ./Jetson-Nano you must define this conn before add in into default keyword arg 
c = conn.cursor()  # you must define this c before add in into default keyword arg 

class controller():
	def __init__(self,ML_DIR_pin = ML_DIR_pin,ML_RUN_pin = ML_RUN_pin,MR_DIR_pin = MR_DIR_pin,MR_RUN_pin = MR_RUN_pin,
					OBS_F_pin = OBS_F_pin,OBS_B_pin = OBS_B_pin,OBS_L_pin = OBS_L_pin,OBS_R_pin = OBS_R_pin,GPIO = RPi.GPIO,
						conn = conn, c = c):
		
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

		self.ESTOP = 0 # estop

		self.GPIO = GPIO

		#initialize gpio
		self.GPIO.setmode(GPIO.BOARD)

		self.GPIO.setup(self.ML_DIR_pin,self.GPIO.OUT)
		self.GPIO.setup(self.ML_RUN_pin,self.GPIO.OUT)
		self.GPIO.setup(self.MR_DIR_pin,self.GPIO.OUT)
		self.GPIO.setup(self.MR_RUN_pin,self.GPIO.OUT)

		# block motors run by EN pins
		self.GPIO.output(self.MR_RUN_pin,0)
		self.GPIO.output(self.ML_RUN_pin,0)
		self.GPIO.output(self.MR_DIR_pin,0)
		self.GPIO.output(self.ML_DIR_pin,0)

		self.GPIO.setup(self.OBS_F_pin,self.GPIO.IN)
		self.GPIO.setup(self.OBS_B_pin,self.GPIO.IN)
		self.GPIO.setup(self.OBS_L_pin,self.GPIO.IN)
		self.GPIO.setup(self.OBS_R_pin,self.GPIO.IN)

		# set database connection and cursor
		self.conn = conn 
		self.c = c 

	def stop(self):
		self.GPIO.output(self.MR_RUN_pin,0)
		self.GPIO.output(self.ML_RUN_pin,0)

	def forward(self):
		self.stop()
		# update all signals for the controller before you run
		self.update_input()
		# print(self.ESTOP)
		if not self.ESTOP:
			self.GPIO.output(self.MR_RUN_pin,1)
			self.GPIO.output(self.ML_RUN_pin,1)
			self.GPIO.output(self.MR_DIR_pin,1)
			self.GPIO.output(self.ML_DIR_pin,1)
		else:
			print('Emergency stop activated! this command can not execute')

	def backward(self):
		self.stop()
		# update all signals for the controller before you run
		self.update_input()
		# print(self.ESTOP)
		if not self.ESTOP:
			self.GPIO.output(self.MR_RUN_pin,1)
			self.GPIO.output(self.ML_RUN_pin,1)
			self.GPIO.output(self.MR_DIR_pin,0)
			self.GPIO.output(self.ML_DIR_pin,0)
		else:
			print('Emergency stop activated! this command can not execute')

	def turnleft(self):
		self.stop()
		# update all signals for the controller before you run
		self.update_input()
		# print(self.ESTOP)
		if not self.ESTOP:
			self.GPIO.output(self.MR_RUN_pin,1)
			self.GPIO.output(self.ML_RUN_pin,1)
			self.GPIO.output(self.MR_DIR_pin,1)
			self.GPIO.output(self.ML_DIR_pin,0)
		else:
			print('Emergency stop activated! this command can not execute')

	def turnright(self):
		self.stop()
		# update all signals for the controller before you run
		self.update_input()
		# print(self.ESTOP)
		if not self.ESTOP:
			self.GPIO.output(self.MR_RUN_pin,1)
			self.GPIO.output(self.ML_RUN_pin,1)
			self.GPIO.output(self.MR_DIR_pin,0)
			self.GPIO.output(self.ML_DIR_pin,1)
		else:
			print('Emergency stop activated! this command can not execute')

	def bit_forward(self,delay):
		self.forward()
		time.sleep(delay)
		self.stop()

	def bit_backward(self,delay):
		self.backward()
		time.sleep(delay)
		self.stop()

	def bit_turnleft(self,delay):
		self.turnleft()
		time.sleep(delay)
		self.stop()

	def bit_turnright(self,delay):
		self.turnright()
		time.sleep(delay)
		self.stop()

	def update_input(self):
		'''
		conn: the connection to database
		c: cusor of the connection to database
		Read the input values
		'''

		self.c.execute("""
			SELECT *FROM robot WHERE id = 1
			""")

		data = self.c.fetchone() # Get all row
		self.conn.commit()

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

		self.c.execute("""
			UPDATE robot
			SET obs_f = ?,
				obs_b = ?,
				obs_l = ?,
				obs_r = ?
			WHERE id = 1
			""",(self.OBS_F_value,self.OBS_B_value,self.OBS_L_value,self.OBS_R_value))

		self.conn.commit()

	def estop(self):
		'''
		This function read the estop value in the database and return it
		'''
		self.c.execute("""
			SELECT *FROM robot WHERE id = 1
			""")

		data = self.c.fetchone() # Get all row
		self.conn.commit()

		# Read ESTOP from the server 
		estop = data[7] # read emergency stop

		return estop

	def obstacles(self):
		'''
		This function read the estop value in the database and return it
		'''
		self.c.execute("""
			SELECT *FROM robot WHERE id = 1
			""")

		data = self.c.fetchone() # Get all row
		self.conn.commit()

		# Read ESTOP from the server 
		obs_f = data[8] # read front ultrasonics sensors
		obs_b = data[9] # read back ultrasonics sensors
		obs_l = data[10] # read left ultrasonics sensors
		obs_r = data[11] # read right ultrasonics sensors

		return obs_f,obs_b,obs_l,obs_r

	def command(self):
		self.c.execute(f"SELECT *FROM robot WHERE id = 1")
		command = self.c.fetchone()[2]
		self.conn.commit()
		return command

if __name__ == "__main__":

	controller = controller() # Create object as default keywords 

	print("Connected to Robot's database via Command Line!")
	# id = int(input('Enter robot ID: '))
	id = 1
	print("Robot is running...")

	while True:

		# Read the command
		command = controller.command()

		# Read the input Allway read the input and write it into the database
		controller.update_input()
		#print(controller.ESTOP,controller.OBS_F_value,controller.OBS_B_value,controller.OBS_L_value,controller.OBS_R_value)

		#Write the output
		if command == "kill":
			print("Stop motor & Clean up")
			break

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
			
		# moving a bit and stop
		# elif command == "bit_forward":
		#	controller.bit_forward()

		# elif command == "bit_backward":
		# 	controller.bit_backward()

		# elif command == "bit_turnleft":
		# 	controller.bit_turnleft()

		# elif command == "bit_turnright":
		#	controller.bit_turnright()

		else:
			print("Command does not Exist!")
			pass

	controller.stop()

	controller.GPIO.cleanup()
	#RPi.GPIO.cleanup()
	
	conn.close()
	
	print("Exit cml")











