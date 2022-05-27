
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
import datetime 
import math  

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

# params for aruco finding
draw_info = True
marker_size = 4
total_markers = 250

# params for give recomment command
S_max = 4000.0 # max square

# inheriate from robot_gpio but no connect to database
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
		return 'left'
	elif current_point[0] > center_point[0] + x_distance:
		return 'right'
	elif (current_point[0] >= center_point[0] - x_distance) & (current_point[0] <= center_point[0] + x_distance):
		return 'center'

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

def calc_aruco(bbox):
	'''
	bbox contain (top_left,top_right,bottom_right,bottom_left)
	this function return centroid of the bbox and square area
	'''
	# find centroid
	centroid = np.mean(bbox,axis = 1).astype('int')
	centroid = tuple(centroid[0])
	# calculate S
	top_left  = bbox[0][0] # top left corner (x,y)
	top_right = bbox[0][1] # top right corner (x,y)
	bottom_right = bbox[0][2] # bottom left corner (x,y)
	bottom_left = bbox[0][3] # bottom right corner (x,y)
	l = math.sqrt((top_right[0]-bottom_left[0])**2+(top_right[1]-bottom_left[1])**2) # the distane between of top-right and bottom-left (x,y)
	m = (top_right[1] - bottom_left[1])/(top_right[0]-bottom_left[0])
	b = top_right[1] - m * top_right[0]
	h1 = abs(m * top_left[0] - top_left[1] + b)/math.sqrt(m**2 + 1)
	h2 = abs(m * bottom_right[0] - bottom_right[1] + b)/math.sqrt(m**2 + 1)
	S = round((0.5*l*h1 + 0.5*l*h2),2)
	return centroid,S

def draw_frame(frame):
	cv2.circle(frame,center_point,10,blue,2) # center point
	cv2.line(frame,(320,220),(320,260),blue,2) # vertical line
	cv2.line(frame,(300,240),(340,240),blue,2) # horizontal line
	cv2.line(frame,(320-vdim,0),(320-vdim,480),blue,2) # vertical frontline left
	cv2.line(frame,(320+vdim,0),(320+vdim,480),blue,2) # vertical frontline right
	cv2.line(frame,(0,240-hdim),(640,240-hdim),blue,2) # horizontal frontline top
	cv2.line(frame,(0,240+hdim),(640,240+hdim),blue,2) # horizontal frontline top

def hunt_aruco_markers(color_frame,depth_frame,target_id,aruco_dict,aruco_param,draw = True):
	'''
	- draw info on screen
	- find aruco
	- give recomment
	'''
	command = 'stop'
	# convert frame to gray
	gray = cv2.cvtColor(color_frame,cv2.COLOR_BGR2GRAY)
	# detect aruco marker
	bboxs,ids,rejected = aruco.detectMarkers(gray,aruco_dict,parameters = aruco_param)
	
	# loop over the results, check condition and draw infomation
	for i,bbox in enumerate(bboxs):
		centroid,S = calc_aruco(bbox)
		# anchor is top right point
		anchor = bbox[0][1].astype('int') # top right point
		distance = depth_frame[anchor[1],anchor[0]]
		if draw:
			# display info in anchor point
			cv2.putText(color_frame, f'{ids[i]}',(anchor[0],anchor[1]-15), cv2.FONT_HERSHEY_SIMPLEX,0.4, green, 1, cv2.LINE_AA)
			cv2.putText(color_frame, f'{centroid}',(anchor[0],anchor[1]), cv2.FONT_HERSHEY_SIMPLEX,0.4, green, 1, cv2.LINE_AA)
			cv2.putText(color_frame, f'{distance}',(anchor[0],anchor[1]+15), cv2.FONT_HERSHEY_SIMPLEX,0.4, green, 1, cv2.LINE_AA)
			cv2.putText(color_frame, f'{S}',(anchor[0],anchor[1]+30), cv2.FONT_HERSHEY_SIMPLEX,0.4, green, 1, cv2.LINE_AA)
			cv2.circle(color_frame,centroid,3,green,-1) # center point
			# draw aruco bounding box
			aruco.drawDetectedMarkers(color_frame,bboxs)
			if ids[i] == target_id:
				cv2.line(color_frame,center_point,centroid,red,2)
				pos = check_LR(center_point,centroid,vdim)
				# base on S and position to give a recomment
				if pos != 'center':
					command = pos 
				else:
					if S < S_max:
						command = 'forward'
					else:
						command ='stop'
				cv2.putText(color_frame,f'P: {pos} S: {S} => {command}',(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.5,green,1,cv2.LINE_AA)

	return command
				

	# give the recomment

def guider(command):
	'''
	Get command then execute
	'''
	current_time = datetime.datetime.now()

	if command != 'stop':
		confirm = input(f'{current_time} Do you want {command}? ')
		if confirm == 'y':
			print(f'{current_time} - {command}')
		else:
			pass
	else:
		pass



# connect to depth camera
d455 = rd.DepthCamera() # initial depth camera object

# init controller gpio 
robot = controller()

# initialize for aruco finding
aruco_key = getattr(aruco,f'DICT_{marker_size}X{marker_size}_{total_markers}')
aruco_dict = aruco.Dictionary_get(aruco_key)
aruco_param = aruco.DetectorParameters_create()

if __name__ == "__main__":

	# Check the connection and try to get data
	ret,depth_frame,color_frame = d455.get_frame()
	
	while ret:
		# read camera 
		ret,depth_frame,color_frame = d455.get_frame()
		
		# convert depth frame
		colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_frame,alpha = 0.08),cv2.COLORMAP_JET)

		# draw info
		if draw_info:
			# read obstacles
			f,b,l,r = robot.read_obstacles()
			cv2.putText(color_frame,f'f:{f} b:{b} l:{l} r:{r}',(10,25),cv2.FONT_HERSHEY_SIMPLEX,0.5,green,1,cv2.LINE_AA)
			draw_frame(color_frame)
	
		# find aruco
		command = hunt_aruco_markers(color_frame,depth_frame,target_id,aruco_dict,aruco_param,draw = draw_info)

		guider(command)

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