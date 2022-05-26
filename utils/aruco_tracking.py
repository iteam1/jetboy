'''
Author: locchuong
Date: 19/4/2022
Descript:
	Tracking specify aruco ID target, run this program at directory: `robot-jetboy`
'''
import cv2  
import cv2.aruco as aruco 
import numpy as np
import realsense_depth as rd # pyrealsense2 package is already in snippet
import RPi.GPIO
import time

# Define pin number
# OUTPUT pins name
ML_DIR_pin = 24 # motor left direction
ML_RUN_pin = 23 # motor left run
MR_DIR_pin = 22 # motor right direction
MR_RUN_pin = 21 # motor right run
# INPUT pins name
OBS_F_pin = 15 # front ultrasonic sensor
OBS_B_pin = 16 # back ultrasonic sensor 
OBS_L_pin = 18 # left ultrasonic sensor 
OBS_R_pin = 19 # right ultrasonic sensor
target_id = 7  # the id robot will track on
# define color
red = (0,0,255)
green = (0,255,0)
blue = (255,0,0)
center_point = (320,240)
vdim = 40
hdim = 30

# Connect with depth camera
d455 = rd.DepthCamera() # initial depth camera
# Check the connection and try to get data
ret,depth_frame,color_frame = d455.get_frame()

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
		f= self.GPIO.input(self.OBS_F_pin)
		b= self.GPIO.input(self.OBS_B_pin)
		l= self.GPIO.input(self.OBS_L_pin)
		r= self.GPIO.input(self.OBS_R_pin)
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

def find_aruco_markers(img,depth,marker_size = 4,total_markers = 250,draw  = True):
	'''
	Find aruco in frame
	Arguments:
		img --- color frame of image
		marker_size --- size of marker default = 4 (4,5,6)
		total_markers --- total markers in frame
		draw --- option to draw marker on the screen
	'''
	centroids = [] # list of centroids marker
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 
	key = getattr(aruco,f'DICT_{marker_size}X{marker_size}_{total_markers}')
	aruco_dict = aruco.Dictionary_get(key)
	aruco_param = aruco.DetectorParameters_create()
	bboxs,ids,rejected = aruco.detectMarkers(gray,aruco_dict, parameters = aruco_param)
	
	# find the centroids list, if bboxs empty, this for loop does not break program
	for i,bbox in enumerate(bboxs):
		
		centroid = np.mean(bbox,axis = 1).astype('int')
		centroid = tuple(centroid[0])
		centroids.append(centroid)

		pt = bbox[0][1].astype('int') # top right
		distance = depth[pt[1],pt[0]]
		
		cv2.putText(img, f'{distance}',(pt[0],pt[1]-15), cv2.FONT_HERSHEY_SIMPLEX,
		0.4, green, 1, cv2.LINE_AA)
		cv2.putText(img, f'{ids[i]}',(pt[0],pt[1]), cv2.FONT_HERSHEY_SIMPLEX,
		0.4, green, 1, cv2.LINE_AA)
		cv2.putText(img, f'{centroid}',(pt[0],pt[1]+15), cv2.FONT_HERSHEY_SIMPLEX,
		0.4, green, 1, cv2.LINE_AA)
		cv2.circle(img,centroid,3,green,-1) # center point
		
		if ids[i] == target_id:
			cv2.putText(img, f'ID{target_id}: {distance} {check_LR(center_point,centroid,vdim)} {check_TB(center_point,centroid,hdim)}',(10,45), cv2.FONT_HERSHEY_SIMPLEX,0.5, green, 1, cv2.LINE_AA)
			cv2.line(img,center_point,centroid,red,2)

	if draw:
		aruco.drawDetectedMarkers(img,bboxs)

def track_aruco_markers(img,depth,target_id,marker_size =4, total_markers =250, draw = True):
	'''
	Tracking aruco 
	'''
	# convert frame to gray
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 
	# init aruco marker
	key = getattr(aruco,f'DICT_{marker_size}X{marker_size}_{total_markers}')
	aruco_dict = aruco.Dictionary_get(key)
	aruco_param = aruco.DetectorParameters_create()
	# find aruco marker
	bboxs,ids,rejected = aruco.detectMarkers(gray,aruco_dict, parameters = aruco_param) # list of np.array,np.array([[]]), list of np.array
	# loop over the ids, if use numpy array ids, there must be error if you get null, so let use list bboxs,
	for i,bbox in enumerate(bboxs):
		# if the id is match target_id
		index = ids[i]
		if index == target_id:
			# find centroid
			centroid = np.mean(bboxs[i],axis = 1).astype('int')
			centroid = tuple(centroid[0])
			# find distance
			pt = bbox[0][1].astype('int') # top right
			distance = depth[pt[1],pt[0]]
			# soon return
			return (centroid,distance,ids[i])
	# return None if you can find nothing
	return None

def recommend_command(img,centroid,distance,display = True):
	'''
	This function return a recommend command for robot
	'''
	h_pos = check_LR(center_point,centroid,vdim)
	if display:
		cv2.putText(img, f'{h_pos}',(10,62), cv2.FONT_HERSHEY_SIMPLEX,0.5,green, 1, cv2.LINE_AA)
	return h_pos			

def draw_frame(frame):
	cv2.circle(frame,center_point,10,blue,2) # center point
	cv2.line(frame,(320,220),(320,260),blue,2) # vertical line
	cv2.line(frame,(300,240),(340,240),blue,2) # horizontal line
	cv2.line(frame,(320-vdim,0),(320-vdim,480),blue,2) # vertical frontline left
	cv2.line(frame,(320+vdim,0),(320+vdim,480),blue,2) # vertical frontline right
	cv2.line(frame,(0,240-hdim),(640,240-hdim),blue,2) # horizontal frontline top
	cv2.line(frame,(0,240+hdim),(640,240+hdim),blue,2) # horizontal frontline top

if __name__ == '__main__':
	# init control gpio object
	robot = controller()
	while ret:
		# read camera
		ret,depth_frame,color_frame = d455.get_frame()
		colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_frame,alpha = 0.08),cv2.COLORMAP_JET)

		# Read obstacles
		f,b,l,r = robot.read_obstacles()
		cv2.putText(color_frame, f'f:{f} b:{b} l:{l} r:{r}',(10,25), cv2.FONT_HERSHEY_SIMPLEX,0.5, green, 1, cv2.LINE_AA)
		
		# find aruco target
		result = track_aruco_markers(color_frame,depth_frame,target_id)
		if result:
			centroid,distance,index  = result[0],result[1],result[2]
			#print(centroid,distance,index)
			r_command = recommend_command(color_frame,centroid,distance)
			if r_command == 'Right':
				#print("robot turn right")
				robot.bit_turnright(0.2)
			elif r_command == 'Left':
				#print("robot turn left")
				robot.bit_turnleft(0.2)
		
		# find aruco in frame
		find_aruco_markers(color_frame,depth_frame)

		# draw info on color_frame
		draw_frame(color_frame)

		# stack depth frame and colorframe
		stack_frame = np.hstack((color_frame,colormap)) # display side by side RGB and Depth next to
	
		# Display color frame
		cv2.imshow('rame',stack_frame)

		if cv2.waitKey(1) == 27:
			break 

	robot.stop()
	robot.GPIO.cleanup()

	d455.release()
	cv2.destroyAllWindows()

