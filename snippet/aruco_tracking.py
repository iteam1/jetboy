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
import sqlite3 
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

# Create the connection to the database and the cursor
conn = sqlite3.connect("./robot/site.db") # ./Jetson-Nano you must define this conn before add in into default keyword arg 
c = conn.cursor()  # you must define this c before add in into default keyword arg

# Connect with depth camera
d455 = rd.DepthCamera() # initial depth camera
# Check the connection and try to get data
ret,depth_frame,color_frame = d455.get_frame()

# inheriate from robot_gpio 
class controller():
	def __init__(self,ML_DIR_pin = ML_DIR_pin,ML_RUN_pin = ML_RUN_pin,MR_DIR_pin = MR_DIR_pin,MR_RUN_pin = MR_RUN_pin,
					OBS_F_pin = OBS_F_pin,OBS_B_pin = OBS_B_pin,OBS_L_pin = OBS_L_pin,OBS_R_pin = OBS_R_pin,GPIO = RPi.GPIO,
						conn = conn, c = c):
		
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

		# set database connection and cursor
		self.conn = conn 
		self.c = c 

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

	def db_stop_update(self):
		'''
		Use this function to set the command in database to stop after bit moving
		'''
		self.c.execute("""
			UPDATE robot
			SET command = "stop"
			WHERE id = 1
			""")
		self.conn.commit()
		
	def bit_forward(self,delay):
		'''
		Motors move abit forward
		'''
		self.forward()
		time.sleep(delay)
		self.stop()
		self.db_stop_update()

	def bit_backward(self,delay):
		'''
		Motors move abit backward
		'''
		self.backward()
		time.sleep(delay)
		self.stop()
		self.db_stop_update()

	def bit_turnleft(self,delay):
		'''
		Motors turn left abit
		'''
		self.turnleft()
		time.sleep(delay)
		self.stop()
		self.db_stop_update()

	def bit_turnright(self,delay):
		'''
		Motor turn right abit
		'''
		self.turnright()
		time.sleep(delay)
		self.stop()
		self.db_stop_update()

	def update_input(self):
		'''
		Use this function to read ESTOP value in database and read sensor values and update it into robot's database
			conn: the connection to database
			c: cusor of the connection to database
		'''

		# Fetch all value columns in database
		self.c.execute("""
			SELECT *FROM robot WHERE id = 1
			""")

		data = self.c.fetchone() # Get all row
		self.conn.commit()

		# Read ESTOP from the server ,write it out to database and storage it into robot object
		self.ESTOP = data[7] # read emergency stop

		# Read ultrasonic sensor signal save it to database
		self.OBS_F_value = self.GPIO.input(self.OBS_F_pin) # read front obstacle value
		self.OBS_B_value = self.GPIO.input(self.OBS_B_pin) # read back obstacle value
		self.OBS_L_value = self.GPIO.input(self.OBS_L_pin) # read left obstacle value
		self.OBS_R_value = self.GPIO.input(self.OBS_R_pin) # read right obstacle value

		# c.execute("""
		# 	INSERT INTO robot(obs_f,obs_b,obs_l,obs_r) VALUES(?,?,?,?)
		# 	""",(self.OBS_F_value,self.OBS_B_value,self.OBS_L_value,self.OBS_B_value))

		# Update the values of sensor into database
		self.c.execute("""
			UPDATE robot
			SET obs_f = ?,
				obs_b = ?,
				obs_l = ?,
				obs_r = ?
			WHERE id = 1
			""",(self.OBS_F_value,self.OBS_B_value,self.OBS_L_value,self.OBS_R_value))
		self.conn.commit()

	def estop(self):
		'''
		This function read the estop value in the database and return it
		'''
		self.c.execute("""
			SELECT *FROM robot WHERE id = 1
			""")

		data = self.c.fetchone() # Get all row
		self.conn.commit()

		# Read ESTOP from the server 
		estop = data[7] # read emergency stop

		return estop

	def obstacles(self):
		'''
		This function read the estop value in the database and return it
		'''
		self.c.execute("""
			SELECT *FROM robot WHERE id = 1
			""")

		data = self.c.fetchone() # Get all row
		self.conn.commit()

		# Read ESTOP from the server 
		obs_f = data[8] # read front ultrasonics sensors
		obs_b = data[9] # read back ultrasonics sensors
		obs_l = data[10] # read left ultrasonics sensors
		obs_r = data[11] # read right ultrasonics sensors

		return obs_f,obs_b,obs_l,obs_r

	def command(self):
		'''
		This function read the command value in database and return it
		'''
		self.c.execute(f"SELECT *FROM robot WHERE id = 1")
		command = self.c.fetchone()[2]
		self.conn.commit()
		return command

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
			0.5, green, 1, cv2.LINE_AA)
			cv2.putText(img, f'{ids[i]}',(pt[0],pt[1]), cv2.FONT_HERSHEY_SIMPLEX,
			0.5, green, 1, cv2.LINE_AA)
			cv2.putText(img, f'{centroid}',(pt[0],pt[1]+15), cv2.FONT_HERSHEY_SIMPLEX,
			0.5, green, 1, cv2.LINE_AA)
			cv2.circle(img,centroid,3,green,-1) # center point
			
			if ids[i] == 7:
				cv2.putText(img, f'ID7: {distance} {check_LR(center_point,centroid,vdim)} {check_TB(center_point,centroid,hdim)}',(50,25), cv2.FONT_HERSHEY_SIMPLEX,1, green, 1, cv2.LINE_AA)
				cv2.line(img,center_point,centroid,red,2)

		if draw:
			aruco.drawDetectedMarkers(img,bboxs)

if __name__ == '__main__':
	while ret:
		ret,depth_frame,color_frame = d455.get_frame()
		colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_frame,alpha = 0.08),cv2.COLORMAP_JET)
		#print(depth_frame.shape)
		
		# find aruco in frame
		find_aruco_markers(color_frame,depth_frame)
		
		# draw info on color_frame
		cv2.circle(color_frame,center_point,10,blue,2) # center point
		cv2.line(color_frame,(320,220),(320,260),blue,2) # vertical line
		cv2.line(color_frame,(300,240),(340,240),blue,2) # horizontal line
		cv2.line(color_frame,(320-vdim,0),(320-vdim,480),blue,2) # vertical frontline left
		cv2.line(color_frame,(320+vdim,0),(320+vdim,480),blue,2) # vertical frontline right
		cv2.line(color_frame,(0,240-hdim),(640,240-hdim),blue,2) # horizontal frontline top
		cv2.line(color_frame,(0,240+hdim),(640,240+hdim),blue,2) # horizontal frontline top

		# Display color frame
		cv2.imshow('color_frame',color_frame)
		cv2.imshow('depth_frame',colormap)

		if cv2.waitKey(1) == 27:
			break 

	d455.release()
	cv2.destroyAllWindows()

