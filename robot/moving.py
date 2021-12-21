'''
Inherentate Robot from GPIO_controller.py
'''
import time 
from GPIO_controller import controller


robot = controller()

if __name__ == '__main__':

	robot.bit_turnleft(0.5)

	time.sleep(2)

	robot.bit_forward(0.2)

	time.sleep(3)

	robot.bit_forward(0.2)

	time.sleep(3)

	robot.bit_forward(0.2)

	time.sleep(3)
