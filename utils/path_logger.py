'''
Author: locchuong
Updated: 28/12/21
Description:
	This python program contain a object connect to GPIO pins and test robot's moving
	without connection to the database, robot will moving follow the instruction from the input
	Also use this program to log the moving command
'''

import sqlite3 
import time
import pynput 
global releaseListening
from pynput.keyboard import Key,Listener 

# log condition y meaning i want to log robot motion, n meaning i don't want log robot motion, else loop until log_con value is y or n
log_con = "a"

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

