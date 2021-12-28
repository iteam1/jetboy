'''
Author: locchuong
Updated: 28/12/21
Description:
	Inherentate from robot_gpio.py controller class, this class connect to robot database, read and update the signal
	Inherentate from test_moving.py
		- contoller, this class ignore robot database
		- read_log, this function will read the log.txt and return a instruction
		- do_log, this function will tell robot do the instruction 
	Robot will move follow the log file
'''
import time 
# from robot.GPIO_controller import controller # run robot.__init__ first
from test_moving import controller, read_log, do_log

print("Test robot moving follow an instruction!")

inter_t = int(input("Enter the interation time: "))

instruction = read_log()

robot = controller()

if __name__ == '__main__':

	do_log(robot,instruction,inter_t)
