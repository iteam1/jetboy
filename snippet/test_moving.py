'''
Author: locchuong
Updated: 27/12/21
Description:
	This python program contain a object connect to GPIO pins and test robot's moving
	without connection to the database, robot will moving follow the instruction from the input
	Also use this program to log the moving command
'''

import RPi.GPIO
import sqlite3 
import time 

# OUTPUT pins name
ML_DIR_pin = 24 # motor left direction
ML_RUN_pin = 23 # motor left run
MR_DIR_pin = 22 # motor right direction
MR_RUN_pin = 21 # motor right run

class controller():
	def __init__(self,ML_DIR_pin = ML_DIR_pin,ML_RUN_pin = ML_RUN_pin,MR_DIR_pin = MR_DIR_pin,MR_RUN_pin = MR_RUN_pin,GPIO = RPi.GPIO):
		
		self.ML_DIR_pin = ML_DIR_pin # driver left dir pin
		self.ML_RUN_pin = ML_RUN_pin # driver left run pin
		self.MR_DIR_pin = MR_DIR_pin # driver right dir pin
		self.MR_RUN_pin = MR_RUN_pin # driver right run pin

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

	def stop(self):
		self.GPIO.output(self.MR_RUN_pin,0)
		self.GPIO.output(self.ML_RUN_pin,0)

	def forward(self):
		self.stop() # this command will stop your robot if you put it in the end of this function
		self.GPIO.output(self.MR_RUN_pin,1)
		self.GPIO.output(self.ML_RUN_pin,1)
		self.GPIO.output(self.MR_DIR_pin,1)
		self.GPIO.output(self.ML_DIR_pin,1)
		
	def backward(self):
		self.stop() # this command will stop your robot if you put it in the end of this function
		self.GPIO.output(self.MR_RUN_pin,1)
		self.GPIO.output(self.ML_RUN_pin,1)
		self.GPIO.output(self.MR_DIR_pin,0)
		self.GPIO.output(self.ML_DIR_pin,0)

	def turnleft(self):
		self.stop() # this command will stop your robot if you put it in the end of this function
		self.GPIO.output(self.MR_RUN_pin,1)
		self.GPIO.output(self.ML_RUN_pin,1)
		self.GPIO.output(self.MR_DIR_pin,1)
		self.GPIO.output(self.ML_DIR_pin,0)

	def turnright(self):
		self.stop() # this command will stop your robot if you put it in the end of this function
		self.GPIO.output(self.MR_RUN_pin,1)
		self.GPIO.output(self.ML_RUN_pin,1)
		self.GPIO.output(self.MR_DIR_pin,0)
		self.GPIO.output(self.ML_DIR_pin,1)
		#self.stop()

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

# Create robot object

robot = controller()

if __name__ == '__main__':

	print("Test controlling robot's moving ")

	print('''
		Command:
			- terminate: x
			- stop : t
			- forward : f
			- backward : b
			- turnleft: l
			- turnright: r
			- bit_forward: w
			- bit_backward: s
			- bit_turnleft: a
			- bit_turnright: d
		''')

	while True:

		command = input("Robot's command? ")

		if command == "x":
			print("Terminate testing robot's moving! ")
			break 

		elif command == "t":
			robot.stop()
			print("Stop")

		elif command == "f":
			robot.forward()
			print("Forward")

		elif command == "b":
			robot.backward()
			print("Backward")

		elif command == "l":
			robot.turnleft()
			print("TurnLeft")

		elif command == "r":
			robot.turnright()
			print("TurnRight")

		elif command == "w":
			robot.bit_forward(0.3)
			print("bit Forward")

		elif command == "s":
			robot.bit_backward(0.3)
			print("bit Backward")

		elif command == "a":
			robot.bit_turnleft(0.1)
			print("bit TurnLeft")

		elif command == "d":
			robot.bit_turnright(0.1)
			print("bit TurnRight")

		else:
			print(f'{command} is not available!')

	print("Done testing!, Exitting...")

	exit()

	robot.GPIO.cleanup()

