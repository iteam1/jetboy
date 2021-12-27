'''
Author: locchuong
Updated: 27/12/21
Description:
Inherentate Robot from GPIO_controller.py
'''
import time 
# from robot.GPIO_controller import controller # run robot.__init__ first
from GPIO_controller import controller


robot = controller()

if __name__ == '__main__':

	for i in range(3):

		robot.bit_turnleft(2.8)

		time.sleep(2)

		robot.bit_forward(1.0)

		time.sleep(2)

		robot.bit_turnright(2.8)

		time.sleep(2)

		robot.bit_forward(1.0)

		time.sleep(2)
