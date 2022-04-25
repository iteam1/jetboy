'''
Author: locchuong
Updated: 28/12/21
Description:
	Inheritance from robot_gpio.py controller class, this class connect to robot database, read and update the signal
	Inheritance from test_moving.py
		- contoller, this class ignore robot database
		- read_log, this function will read the log.txt and return a instruction
		- do_log, this function will tell robot do the instruction 
	Robot will move follow the log file
'''
import time
import RPi.GPIO
from robot_gpio import controller # you must run this code in the directory ./Jetson-Nano python3 ./snippet/moving.py
# from robot.GPIO_controller import controller # run robot.__init__ first
# from test_moving import controller

# OUTPUT pins name
ML_DIR_pin = 24 # motor left direction
ML_RUN_pin = 23 # motor left run
MR_DIR_pin = 22 # motor right direction
MR_RUN_pin = 21 # motor right run

def read_log(path,mode):
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

print("Test robot moving follow an instruction!")

inter_t = int(input("Enter the interation time: "))

log_file = input("Where is the instruction? ")

print("Do the instruction: "+ log_file )

instruction = read_log(log_file,"r")

#robot = gpio_controller()
robot = controller()

if __name__ == '__main__':

	do_log(robot,instruction,inter_t)
