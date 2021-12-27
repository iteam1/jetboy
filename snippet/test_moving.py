'''
Author: locchuong
Updated: 27/12/21
Description:
This python program contain a object connect to GPIO pins and test robot's moving
without connection to the database, robot will moving follow the instruction from the input

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
	def __init__(self,ML_DIR_pin = ML_DIR_pin,ML_RUN_pin = ML_RUN_pin,MR_DIR_pin = MR_DIR_pin,MR_RUN_pin = MR_RUN_pin,
					OBS_F_pin = OBS_F_pin,OBS_B_pin = OBS_B_pin,OBS_L_pin = OBS_L_pin,OBS_R_pin = OBS_R_pin,GPIO = RPi.GPIO):
		
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
		self.GPIO.output(self.MR_RUN_pin,1)
		self.GPIO.output(self.ML_RUN_pin,1)
		self.GPIO.output(self.MR_DIR_pin,1)
		self.GPIO.output(self.ML_DIR_pin,1)
		self.stop()


	def backward(self):
		self.GPIO.output(self.MR_RUN_pin,1)
		self.GPIO.output(self.ML_RUN_pin,1)
		self.GPIO.output(self.MR_DIR_pin,0)
		self.GPIO.output(self.ML_DIR_pin,0)
		self.stop()

	def turnleft(self):
		self.GPIO.output(self.MR_RUN_pin,1)
		self.GPIO.output(self.ML_RUN_pin,1)
		self.GPIO.output(self.MR_DIR_pin,1)
		self.GPIO.output(self.ML_DIR_pin,0)
		self.stop()

	def turnright(self):
		self.GPIO.output(self.MR_RUN_pin,1)
		self.GPIO.output(self.ML_RUN_pin,1)
		self.GPIO.output(self.MR_DIR_pin,0)
		self.GPIO.output(self.ML_DIR_pin,1)
		self.stop()

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


