'''
Author: locchuong
Updated: 27/6/22
Description:
	Update calculation function 
	This is contain routes of the flask server
'''
from flask import render_template,request,Response,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import cv2
import cv2.aruco as aruco 
import numpy as np
#import robot.realsense_depth as rd
from robot import app,db,d455
from robot import pc,points,colorizer # for pointcloud capture
from robot.models import Robot
import math
import datetime

# define color
red = (0,0,255)
green = (0,255,0)
blue = (255,0,0)
center_point = (320,240)
vdim = 40 # vertical distance for gen_cvframe
hdim = 40 # horizontal distance for gen_cvframe

# shutdown function
def shutdown_server():
	func = request.environ.get('werkzeug.server.shutdown')
	if func is None:
		raise RunTimeError('Not running with Werkzeug Server')
	func()

# Generate frame with computer vision functionality
def gen_cvframe():
	'''
	This function stream frame with computer vision functionality
	'''

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


	# support function for cvframe
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
	
	# support function for cvframe
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
	
	# support function for cvframe
	def find_aruco_markers(img,depth,marker_size = 4,total_markers = 250,draw  = True):
		'''
		Find aruco in frame
		Arguments:
			img --- color frame of image
			marker_size --- size of marker default = 4 (4,5,6)
			total_markers --- total markers in frame
			draw --- option to draw marker on the screen
		'''
		#centroids = [] # list of centroids marker
		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 
		key = getattr(aruco,f'DICT_{marker_size}X{marker_size}_{total_markers}')
		aruco_dict = aruco.Dictionary_get(key)
		aruco_param = aruco.DetectorParameters_create()
		bboxs,ids,rejected = aruco.detectMarkers(gray,aruco_dict, parameters = aruco_param)
		
		# find the centroids list, if bboxs empty, this for loop does not break program
		for i,bbox in enumerate(bboxs):
			
			centroid,S = calc_aruco(bbox)# np.mean(bbox,axis = 1).astype('int')
			# centroid = tuple(centroid[0])
			# centroids.append(centroid)

			pt = bbox[0][1].astype('int') # top right
			distance = depth[pt[1],pt[0]]
			
			cv2.putText(img, f'{distance}',(pt[0],pt[1]-15), cv2.FONT_HERSHEY_SIMPLEX,
			0.5, green, 1, cv2.LINE_AA)
			cv2.putText(img, f'{ids[i]}',(pt[0],pt[1]), cv2.FONT_HERSHEY_SIMPLEX,
			0.5, green, 1, cv2.LINE_AA)
			cv2.putText(img, f'{centroid}',(pt[0],pt[1]+15), cv2.FONT_HERSHEY_SIMPLEX,
			0.5, green, 1, cv2.LINE_AA)
			cv2.putText(img, f'{S}',(pt[0],pt[1]+25), cv2.FONT_HERSHEY_SIMPLEX,
			0.5, green, 1, cv2.LINE_AA)
			cv2.circle(img,centroid,3,green,-1) # center point
			
			if ids[i] == 7:
				cv2.putText(img, f'ID7: {distance} | {check_LR(center_point,centroid,vdim)} | {check_TB(center_point,centroid,hdim)} | {S}',(10,20), cv2.FONT_HERSHEY_SIMPLEX,0.5, green, 1, cv2.LINE_AA)
				cv2.line(img,center_point,centroid,red,2)

		if draw:
			aruco.drawDetectedMarkers(img,bboxs)

	while True:
		ret,depth_frame,color_frame,frames = d455.get_frame()
		colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_frame,alpha = 0.08),cv2.COLORMAP_JET)
		if not ret:
			print('Connection to camera failed!')
			break 
		else:

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

			#obs_f,obs_b,obs_l,obs_r  = db_read_obstacles(conn,c)
			#cv2.putText(color_frame, f'f: {f} b: {b} l: {l} r: {r}',(10,40), cv2.FONT_HERSHEY_SIMPLEX,0.5, green, 1, cv2.LINE_AA)			

			# Rendering
			stack_frame = np.hstack((color_frame,colormap)) # display side by side RGB and Depth next to
  
			success,buffer = cv2.imencode('.jpg',stack_frame)
			frame = buffer.tobytes()

			yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def gen_colorframe():
	while True:
		ret,depth_frame,color_frame,frames = d455.get_frame()
		if not ret:
			print('Connection to camera failed!')
			break 
		else:
			success,buffer = cv2.imencode('.jpg',color_frame)
			frame = buffer.tobytes()

			yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Generate depth frame
def gen_depthframe():
	while True:
		ret,depth_frame,color_frame,frames = d455.get_frame()

		depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_frame,alpha=0.08),cv2.COLORMAP_JET)
		if not ret:
			print("Connection to camera failed!")
			break
		else:
			success,buffer = cv2.imencode('.jpg',depth_colormap)
			frame = buffer.tobytes()

			yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#Generate depth frame and color frame
def gen_both():
	while True:
		ret,depth_frame,color_frame,frames = d455.get_frame()

		# In the heat map conversion
		depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_frame,alpha = 0.08),cv2.COLORMAP_JET)

		# Rendering
		images = np.hstack((color_frame,depth_colormap)) # display side by side RGB and Depth next to
  
		if not ret:
			print("Connection to camera failed!")
			break
		else:
			success,buffer = cv2.imencode('.jpg',images)
			frame = buffer.tobytes()

			yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/",methods =['GET'])
def home():
    return render_template("home.html")

@app.route("/manual",methods = ['GET','POST'])
def manual():
	if request.method == 'POST':
		command = request.form.get('command') # If null then not error occur
		if command:
			myrobot = Robot.query.get(1)
			myrobot.command = command
			estop = myrobot.estop # query estop value
			db.session.commit()
			flash(f'Robot {command}','info')
		return  redirect(url_for('manual'))
		render_template('manual.html',estop)
	myrobot = Robot.query.get(1)
	estop = myrobot.estop # query estop value	
	return render_template('manual.html',estop = estop)

@app.route('/color')
def colorstream():
	return Response(gen_colorframe(),mimetype = 'multipart/x-mixed-replace; boundary=frame')

@app.route('/depth')
def depthstream():
	return Response(gen_depthframe(),mimetype = 'multipart/x-mixed-replace; boundary=frame')

@app.route('/cv')
def cvstream():
	return Response(gen_cvframe(),mimetype = 'multipart/x-mixed-replace; boundary=frame')

@app.route('/content',methods =['POST'])
def content():
	'''
	change display screen to display a content for robot_gui 
	'''
	#if request.method == 'POST':
	content = request.form.get('content')
	myrobot = Robot.query.get(1)
	myrobot.itype = 'info'
	myrobot.content = content
	estop = myrobot.estop # query estop value	
	db.session.commit()
	return render_template('manual.html',estop = estop)
	
@app.route('/emotion',methods =['POST'])
def emotion():
	'''
	change display screen to emotion for robot_gui 
	'''
	emotion = request.form.get('emotion')
	myrobot = Robot.query.get(1)
	myrobot.itype = 'emo'
	myrobot.emotion = emotion
	estop = myrobot.estop # query estop value	
	db.session.commit()
	return render_template('manual.html',estop = estop)
	
@app.route('/image',methods =['POST'])
def image():
	'''
	change display screen to image for robot_gui 
	'''
	image = request.form.get('image')
	myrobot = Robot.query.get(1)
	myrobot.itype = 'img'
	myrobot.image = image
	estop = myrobot.estop # query estop value	
	db.session.commit()
	return render_template('manual.html',estop = estop)

@app.route('/estop',methods = ['POST'])
def estop():
	'''
	Read estop in database, if estop = 1 set estop = 0
	if estop = 0, set estop = 1
	'''
	#if request.method == 'POST':
	myrobot = Robot.query.get(1)
	if myrobot.estop == 0:
		myrobot.estop = 1
		db.session.commit()
		return render_template('manual.html',estop = myrobot.estop)
	else:
		myrobot.estop = 0
		db.session.commit()
		return render_template('manual.html',estop = myrobot.estop)

@app.route('/shutdown',methods = ['POST'])
def shutdown():
	shutdown_server()
	return 'Server shutting down'

# capture frame
@app.route("/capture_img",methods = ['POST'])
def capture_img():
	# get current frame
	ret,depth_frame,color_frame,frames = d455.get_frame()
	now = datetime.datetime.now()
	now = now.isoformat().replace(".","-")
	now = "./imgs/" + now + ".jpg"
	cv2.imwrite(now,color_frame)
	# update estop
	myrobot = Robot.query.get(1)
	estop = myrobot.estop # query estop value	
	return render_template('manual.html',estop = estop)