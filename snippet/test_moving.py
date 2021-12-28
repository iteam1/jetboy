'''
Author: locchuong
Updated: 28/12/21
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

# log condition y meaning i want to log robot motion, n meaning i don't want log robot motion, else loop until log_con value is y or n
log_con = "a"

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

# Logger function
def create_log():
	'''
	Create a log.txt
	'''
	with open("log.txt",'w') as f:
		print("Created log.txt")

def add_log(message):
	'''
	Write into log.txt file everytime you press 
	If you use 'w' meaning write mode, it will create a log.txt file if you don't have one
	If you use 'a' meaning append mode, it will append log.txt 's content 
	If the log_con = y it will log the key presses, else pass
	'''
	global log_con
	if log_con == "y":
		with open("log.txt","a") as f:
			f.write(message)
			f.write("\n")
	else: 
		pass

def read_log(path = "./log.txt",mode = "r"):
	'''
	Read the log file and return a list of moving, this is the instruction, robot will read this instruction and do like this instruction
	'''
	instruction = []
	f = open(path,mode)
	content = f.read()
	e = content.split("\n") # return a list
	for i in e:
		move =  i.split("@")
		instruction.append(move[-1])

	return instruction
# Unkeyword arguments meaning uninitial value
def do_log(robot,instruction,inter_t):

	'''
	Read the instruction and make robot do follow it
	'''
	print(instruction)

	for move in instruction:
		if move == 'bit_forward':
			print(f'robot {move}')
			robot.bit_forward(0.3)
		elif move == 'bit_backward':
			print(f'robot {move}')
			robot.bit_backward(0.3)
		elif move == 'bit_turnleft':
			print(f'robot {move}')
			robot.bit_turnleft(0.1)
		elif move == 'bit_turnright':
			print(f'robot {move}')
			robot.bit_turnright(0.1)
		elif move == 'exit':
			robot.stop()
			print("The instruction is completed.")
			exit()
		else:
			print("This move is not avaiable!")

		time.sleep(inter_t) # Robot must take this time to do the instruction


# Key listener function
def on_press(key): 
	global robot
	# print("{0} pressed".format(key.char))
	if key == Key.up:
		m = " [ " + str(time.asctime()) + " ]@" + "bit_forward"
		print(m)
		add_log(m)
		robot.bit_forward(0.3)
	elif key == Key.down:
		m = " [ " + str(time.asctime()) + " ]@" + "bit_backward"
		print(m)
		add_log(m)
		robot.bit_backward(0.3)
	elif key == Key.left:
		m = " [ " + str(time.asctime()) + " ]@" + "bit_turnleft"
		print(m)
		add_log(m)
		robot.bit_turnleft(0.1)
	elif key == Key.right:
		m = " [ " + str(time.asctime()) + " ]@" + "bit_turnright"
		print(m)
		add_log(m)
		robot.bit_turnright(0.1)
	elif key == Key.esc:
		m = " [ " + str(time.asctime()) + " ]@" + "exit"
		print(m)
		add_log(m)
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

	while True:
		log_con = input("Do you want to log robot motion [y/n]? ")
		if log_con == "y" or log_con == "n":
			print(f"Log's robot's motion: {log_con}")
			break

	if log_con == "y":
		create_log()

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

