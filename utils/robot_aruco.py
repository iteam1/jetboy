
'''
Author: locchuong
Date: 30/6/2022
Descript:
	- robot auto find and go to specific id
	- stop when get obstacles 
	- auto find target
	- timestep delay
	- capture frame
	- opencv compare frame
'''
import cv2
import cv2.aruco as aruco 
import numpy as np
import realsense_depth as rd 
import RPi.GPIO 
import time
import datetime 
import math
import argparse

# init parser
parser = argparse.ArgumentParser(description = 'tracking aruco marker')
# add argument to parser
parser.add_argument('-d','--display', action = 'store_true', help = 'option to display frame')
parser.add_argument('-p','--print', action = 'store_false', help = 'option to do not print out frame')
parser.add_argument('-i','--id', type = int, required = True,help  = 'the target id')
parser.add_argument('-r','--tr', type = float, required = False, default = 0.4, help  = 'timestep rotate')
parser.add_argument('-l','--tl', type = float, required = False, default = 0.2, help  = 'timestep linear')
parser.add_argument('-t','--td', type = float, required = False,help = 'time delay')
# create arguments
args = parser.parse_args()

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

# define color 
red = (0,0,255)
green = (0,255,0)
blue = (255,0,0)

# define point
vdim = 40 
hdim = 40
f_width = 640
f_height = 480
center_point = (int(f_width/2),int(f_height/2)) # x_max = 640, y_max = 480

# params for aruco finding
marker_size = 4
total_markers = 250

# params for give recomment command
S_max = 4000.0 # max square

# init some variable
command = 'stop' # command action 
timestamp = datetime.datetime.now() # define timestamp
pos = "Unknown" # position for robot
S = 0.0 # square erea of the target marker
distance = 0.0 # distance of the target marker

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
	if current_point[0] < (center_point[0] - x_distance):
		return 'left'
	elif current_point[0] > (center_point[0] + x_distance):
		return 'right'
	elif (current_point[0] >= (center_point[0] - x_distance)) & (current_point[0] <= (center_point[0] + x_distance)):
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
	if current_point[1] < (center_point[1] - y_distance):
		return 'top'
	elif current_point[1] > (center_point[1] + y_distance):
		return 'bottom'
	elif (current_point[1] >= (center_point[1] - y_distance)) & (current_point[1] <= (center_point[1] + y_distance)):
		return 'center'

def calc_aruco(bbox):
	'''
	bbox contain (top_left,top_right,bottom_right,bottom_left)
	this function return centroid of the bbox and square area
	Arguments:
		bbox --- the marker bounding box
	Return:
		centroid --- centroid of the marker
		S --- square area of the marker
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
	'''
	Read obstacle and draw on frame
	'''
	f,b,l,r = robot.read_obstacles()
	cv2.putText(color_frame,f'f:{f} b:{b} l:{l} r:{r}',(10,25),cv2.FONT_HERSHEY_SIMPLEX,0.5,green,1,cv2.LINE_AA)
	cv2.circle(frame,center_point,10,blue,2) # center point
	
	cv2.line(frame,(int(f_width/2),int(f_height/2-vdim/2)),(int(f_width/2),int(f_height/2-vdim/2)),blue,2) # vertical line
	cv2.line(frame,(int(f_width/2)-hdim,f_height),(int(f_width/2)+hdim,f_height),blue,2) # horizontal line
	
	cv2.line(frame,(int(f_width/2)-vdim,0),(int(f_width/2-vdim),f_height),blue,2) # vertical frontline left
	cv2.line(frame,(int(f_width/2+vdim),0),(int(f_width/2+vdim),f_height),blue,2) # vertical frontline right
	
	cv2.line(frame,(0,int(f_height/2)-hdim),(f_width,int(f_height/2)-hdim),blue,2) # horizontal frontline top
	cv2.line(frame,(0,int(f_height/2)+hdim),(f_width,int(f_height/2)+hdim),blue,2) # horizontal frontline bottom

def find_aruco_markers(color_frame,depth_frame,marker_size = 4,total_markers = 250,draw  = True):
	'''
	This function detect every marker in frame, if marker id is the same with your specific
	id then draw the pointing line
	Arguments:
		color_frame --- camera's color frame
		depth_frame --- camera's depth frame
		marker_size --- default = 4
		total_markers --- default = 250
		draw --- default True
	Return:
		pos --- postion of the marker
		S --- Square area of the marker
		centroid --- centroid of the marker have target id
	'''
	gray = cv2.cvtColor(color_frame,cv2.COLOR_BGR2GRAY) # convert your image to gray color
	bboxs,ids,rejected = aruco.detectMarkers(gray,aruco_dict, parameters = aruco_param) # detect aruco targets
	for i,bbox in enumerate(bboxs):
		'''
		Calculate centroid and S for every marker
		'''
		centroid,S = calc_aruco(bbox)
		# anchor is top right point
		anchor = bbox[0][1].astype('int') # top right point
		distance = depth_frame[anchor[1],anchor[0]]
		if draw:
			# display info in anchor point
			cv2.putText(color_frame, f'{ids[i]}',(anchor[0],anchor[1]-15), cv2.FONT_HERSHEY_SIMPLEX,0.4, green, 2, cv2.LINE_AA)
			cv2.putText(color_frame, f'{centroid}',(anchor[0],anchor[1]), cv2.FONT_HERSHEY_SIMPLEX,0.4, green, 2, cv2.LINE_AA)
			cv2.putText(color_frame, f'{distance}',(anchor[0],anchor[1]+15), cv2.FONT_HERSHEY_SIMPLEX,0.4, green, 2, cv2.LINE_AA)
			cv2.putText(color_frame, f'{S}',(anchor[0],anchor[1]+30), cv2.FONT_HERSHEY_SIMPLEX,0.4, green, 2, cv2.LINE_AA)
			cv2.circle(color_frame,centroid,3,green,-1) # center point
			'''
			If the ids is equal to your specific id
			'''
			if ids[i] == args.id:
				pos = check_LR(center_point,centroid,hdim) # horizontal
				cv2.line(color_frame,center_point,centroid,red,2)
				cv2.putText(color_frame,f'P: {pos} S: {S} => ',(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.5,green,1,cv2.LINE_AA)
				return pos,S,centroid
	return None

	if draw:
		aruco.drawDetectedMarkers(color_frame,bboxs)
	
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
		result = find_aruco_markers(color_frame,depth_frame,args.id,aruco_dict,aruco_param)

		# read sensor obstacle value
		f,b,l,r = robot.read_obstacles()

		# update timestamp
		timestamp = datetime.datetime.now()

		# decide the action
		if result: # if we got re soon return
			pos = result[0]
			S = result[1]
			centroid = result[2] # y,x
			distance = depth_frame[centroid[1],centroid[0]] # x,y
			if pos == 'center':
				if S < S_max:
					command = 'forward'
					robot.bit_forward(args.tl)
				else:
					command = 'stop'
			elif pos == 'right':
				command = 'turnright'
				robot.bit_turnright(args.tr)
			elif pos == 'left':
				command = 'turnleft'
				robot.bit_turnleft(args.tr)
		# if we don't find out the marker
		else:
			pos = "Unknown"
			S = 0.0
			centroid = (0,0) # y,x
			distance = 0.0 # x,y
			command = 'stop'


			
		# printout the action
		if args.print: # already true
			print(f'{timestamp} - {pos} - {command} - {S} - {distance} - [f={f},b={b},l={l},r={r}]')

		# display color frame
		if args.display: # already false
			draw_frame(color_frame)
			# stack depth frame and colorframe
			stack_frame = np.hstack((color_frame,colormap)) # display depth_frame and color_frame side by side
			cv2.imshow('frame',stack_frame)
		
		# delay
		# if args.td:
		# 	time.sleep(args.td)

		# wait frame millisecond
		if cv2.waitKey(int(args.td)) == 27:
			break 

	# stop manipulate gpio 
	robot.stop()
	robot.GPIO.cleanup()

	# release
	d455.release()
	cv2.destroyAllWindows()
