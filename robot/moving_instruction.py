'''
Inherentate Robot from GPIO_controller.py
'''
from GPIO_controller import controller


robot = controller()

if __name__ == '__main__':

	robot.bit_forward(0.1)

	robot.bit_forward(0.2)

	robot.bit_forward(0.2)