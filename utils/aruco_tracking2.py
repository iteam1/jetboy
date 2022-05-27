
'''
Author: locchuong
Date: 27/5/2022
Descript:
	Tracking specify aruco ID target, find the way go to that target
'''
import cv2
import cv2.aruco as aruco 
import numpy as np
import realsense_depth as rd 
import RPi.GPIO 
import time   

# Define pin number
# output pin name
ML_DIR_pin = 24 # motor left direction
ML_RUN_pin = 23 # motor left run 
MR_DIR_pin = 22 # motor right direction 
MR_RUN_pin = 21 # motor right run

# input pin name 
OBS_F_pin = 15 # front ultrasonic sensor
OBS_B_pin = 16 # back ultrasonic sensor
OBS_L_pin = 18 # left ultrasonic sensor
OBS_R_pin = 19 # right ultrasonic sensor
target_id = 7 # the specific id robot will track on

# define color 
red = (0,0,255)
green = (0,255,0)
blue = (255,0,0)
center_point = (320,240) # x_max = 640, y_max = 480
vdim = 40 
hdim = 30

class controller():
	def __init__(self,ML_DIR_pin = ML_DIR_pin,ML_RUN_pin = ML_RUN_pin,MR_DIR_pin = MR_DIR_pin,MR_RUN_pin = MR_RUN_pin,
					OBS_F_pin = OBS_F_pin,OBS_B_pin = OBS_B_pin,OBS_L_pin = OBS_L_pin,OBS_R_pin = OBS_R_pin,GPIO = RPi.GPIO):
		
		self.ML_DIR_pin = ML_DIR_pin # driver left dir pin
		self.ML_RUN_pin = ML_RUN_pin # driver left run pin
		self.MR_DIR_pin = MR_DIR_pin # driver right dir pin
		self.MR_RUN_pin = MR_RUN_pin # driver right run pin

		self.OBS_F_pin = OBS_F_pin # front obstacle pin
		self.OBS_F_value = 0 # front obstacle value
		self.OBS_B_pin = OBS_B_pin # back obstacle pin
		self.OBS_B_value = 0 # back obstacle value  
		self.OBS_L_pin = OBS_L_pin # left obstacle pin
		self.OBS_L_value = 0 # left obstacle value
		self.OBS_R_pin = OBS_R_pin # right obstacle pin
		self.OBS_R_value = 0 # right obstacle value

		self.ESTOP = 0 # estop value 0 = O.K, 1 = STOP NOW
		self.GPIO = GPIO

		#initialize gpio
		self.GPIO.setmode(GPIO.BOARD) # Set the pin's definition mode
		
		# Define I/O for motor control pins
		self.GPIO.setup(self.ML_DIR_pin,self.GPIO.OUT)
		self.GPIO.setup(self.ML_RUN_pin,self.GPIO.OUT)
		self.GPIO.setup(self.MR_DIR_pin,self.GPIO.OUT)
		self.GPIO.setup(self.MR_RUN_pin,self.GPIO.OUT)
		
		# Define I/O for sensor control pins
		self.GPIO.setup(self.OBS_F_pin,self.GPIO.IN)
		self.GPIO.setup(self.OBS_B_pin,self.GPIO.IN)
		self.GPIO.setup(self.OBS_L_pin,self.GPIO.IN)
		self.GPIO.setup(self.OBS_R_pin,self.GPIO.IN)

		# block motors run by EN pins
		self.GPIO.output(self.MR_RUN_pin,0)
		self.GPIO.output(self.ML_RUN_pin,0)
		self.GPIO.output(self.MR_DIR_pin,0)
		self.GPIO.output(self.ML_DIR_pin,0)

	def stop(self):
		'''
		Stop motor immediately
		'''
		self.GPIO.output(self.MR_RUN_pin,0)
		self.GPIO.output(self.ML_RUN_pin,0)

	def forward(self):
		'''
		Motor run forward continously
		'''
		self.stop()
		# update all signals for the controller before you run
		#self.update_input()
		# print(self.ESTOP)
		if not self.ESTOP:
			self.GPIO.output(self.MR_DIR_pin,1)
			self.GPIO.output(self.ML_DIR_pin,1)
			self.GPIO.output(self.MR_RUN_pin,1)
			self.GPIO.output(self.ML_RUN_pin,1)			
		else:
			print('Emergency stop activated! this command can not execute')

	def backward(self):
		'''
		Motor run backward continously
		'''
		self.stop()
		# update all signals for the controller before you run
		#self.update_input()
		# print(self.ESTOP)
		if not self.ESTOP:
			self.GPIO.output(self.MR_DIR_pin,0)
			self.GPIO.output(self.ML_DIR_pin,0)
			self.GPIO.output(self.MR_RUN_pin,1)
			self.GPIO.output(self.ML_RUN_pin,1)			
		else:
			print('Emergency stop activated! this command can not execute')

	def turnleft(self):
		'''
		Motor turn left continously
		'''
		self.stop()
		# update all signals for the controller before you run
		#self.update_input()
		# print(self.ESTOP)
		if not self.ESTOP:
			self.GPIO.output(self.MR_DIR_pin,1)
			self.GPIO.output(self.ML_DIR_pin,0)
			self.GPIO.output(self.MR_RUN_pin,1)
			self.GPIO.output(self.ML_RUN_pin,1)
		else:
			print('Emergency stop activated! this command can not execute')

	def turnright(self):
		'''
		Motor turn right continously
		'''
		self.stop()
		# update all signals for the controller before you run
		#self.update_input()
		# print(self.ESTOP)
		if not self.ESTOP:
			self.GPIO.output(self.MR_DIR_pin,0)
			self.GPIO.output(self.ML_DIR_pin,1)
			self.GPIO.output(self.MR_RUN_pin,1)
			self.GPIO.output(self.ML_RUN_pin,1)
		else:
			print('Emergency stop activated! this command can not execute')
		
	def bit_forward(self,delay):
		'''
		Motors move abit forward
		'''
		self.forward()
		time.sleep(delay)
		self.stop()

	def bit_backward(self,delay):
		'''
		Motors move abit backward
		'''
		self.backward()
		time.sleep(delay)
		self.stop()

	def bit_turnleft(self,delay):
		'''
		Motors turn left abit
		'''
		self.turnleft()
		time.sleep(delay)
		self.stop()

	def bit_turnright(self,delay):
		'''
		Motor turn right abit
		'''
		self.turnright()
		time.sleep(delay)
		self.stop()

	def read_obstacles(self):
		# read values
		f = self.GPIO.input(self.OBS_F_pin)
		b = self.GPIO.input(self.OBS_B_pin)
		l = self.GPIO.input(self.OBS_L_pin)
		r = self.GPIO.input(self.OBS_R_pin)
		# update in object variable
		self.OBS_F_value = f 
		self.OBS_B_value = b 
		self.OBS_L_value = l 
		self.OBS_R_value = r 
		return f,b,l,r

def check_LR(center_point,current_point,x_distance):
	'''
	Check the position of target
	Arguments:
		center_point --- center point on the screen
		current_point --- current position of the aruco
		x_distance --- the acceptable distance 
	Return:
		(string) left right or center
	'''
	if current_point[0] < center_point[0] - x_distance:
		return 'Left'
	elif current_point[0] > center_point[0] + x_distance:
		return 'Right'
	elif (current_point[0] >= center_point[0] - x_distance) & (current_point[0] <= center_point[0] + x_distance):
		return 'Center'

def check_TB(center_point,current_point,y_distance):
	'''
	Check the position of target
	Arguments:
		center_point --- center point on the screen
		current_point --- current position of the aruco
		y_distance --- the acceptable distance 
	Return:
		(string) top bottom or center
	'''
	if current_point[1] < center_point[1] - y_distance:
		return 'Top'
	elif current_point[1] > center_point[1] + y_distance:
		return 'Bottom'
	elif (current_point[1] >= center_point[1] - y_distance) & (current_point[1] <= center_point[1] + y_distance):
		return 'Center'

# connect to depth camera
d455 = rd.DepthCamera() # initial depth camera object
# Check the connection and try to get data
ret,depth_frame,color_frame = d455.get_frame()

# inheriate from robot_gpio but no connect to database

if __name__ == "__main__":
	# init controller gpio 
	robot = controller()

	while ret:
		# read camera 
		ret,depth_frame,color_frame = d455.get_frame()
		# convert depth frame
		colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_frame,alpha = 0.08),cv2.COLORMAP_JET)
		# read obstacles
		f,b,l,r = robot.read_obstacles()
		cv2.putText(color_frame,f'f:{f} b:{b} l:{l} r:{r}',(10,25),
			cv2.FONT_HERSHEY_SIMPLEX,0.5,green,1,cv2.LINE_AA)
		# stack depth frame and colorframe
		stack_frame = np.hstack((color_frame,colormap)) # display depth_frame and color_frame side by side
		# display color frame
		cv2.imshow('frame',stack_frame)
		# wait frame
		if cv2.waitKey(1) == 27:
			break 

	# stop manipulate gpio 
	robot.stop()
	robot.GPIO.cleanup()

	# release
	d455.release()
	cv2.destroyAllWindows()