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
import pynput 
global releaseListening
from pynput.keyboard import Key,Listener 

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

# Key logger function

def create_file():
	with open("log.txt",'w') as f:
		print("Created log.txt")


def log(message):
	'''
	If you use 'w' meaning write mode, it will create a log.txt file if you don't have one
	If you use 'a' meaning append mode, it will append log.txt 's content  
	'''
	with open("log.txt","a") as f:
		f.write(message)
		f.write("\n")

def on_press(key): 
	global robot
	# print("{0} pressed".format(key.char))
	if key == Key.up:
		m = " [ " + str(time.asctime()) + " ]@" + "bit_forward"
		print(m)
		log(m)
		robot.bit_forward(0.3)
	elif key == Key.down:
		m = " [ " + str(time.asctime()) + " ]@" + "bit_backward"
		print(m)
		log(m)
		robot.bit_backward(0.3)
	elif key == Key.left:
		m = " [ " + str(time.asctime()) + " ]@" + "bit_turnleft"
		print(m)
		log(m)
		robot.bit_turnleft(0.1)
	elif key == Key.right:
		m = " [ " + str(time.asctime()) + " ]@" + "bit_turnright"
		print(m)
		log(m)
		robot.bit_turnright(0.1)
	elif key == Key.esc:
		m = " [ " + str(time.asctime()) + " ]@" + "Exit now ..."
		print(m)
		log(m)
		robot.stop()
		robot.GPIO.cleanup()
		exit()
	else:
		print("{0} is not available!".format(key))

def on_release(key):
	if key == Key.esc:
		return False # Return false will break the loop

if __name__ == '__main__':

	print("Test controlling robot's moving ")

	create_file()

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
		listening...
		''')

	with Listener(on_press = on_press, on_release = on_release) as listener:
		listener.join()

	print("Done testing!, Exitting...")

	robot.GPIO.cleanup()

	exit()

