'''
Author: locchuong
Updated: 1/8/22
Description:
	Update calculation function 
	This is contain routes of the flask server
'''

#BASIC FUNCTION
from flask import render_template,request,Response,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import cv2
import numpy as np
from robot import app,db,d455
from robot import pc,points,colorizer # for pointcloud capture
from robot.pyrealsense2 import pyrealsense2 as rs
from robot.models import Robot
import math
import datetime
#FACE-RECOGNITION
import face_recognition

#FACE-RECOGNITION
font = cv2.FONT_HERSHEY_DUPLEX # cv2.FONT_HERSHEY_SIMPLEX

# load a sample picture and learn how to recognize it.
cuong_image = face_recognition.load_image_file('./utils/faces/cuong.png')
cuong_face_encoding = face_recognition.face_encodings(cuong_image)[0]

loc_image = face_recognition.load_image_file('./utils/faces/loc.png')
loc_face_encoding = face_recognition.face_encodings(loc_image)[0]

# create arrays of know face encodings and their names
known_face_encodings = [cuong_face_encoding,loc_face_encoding]

# create a list of names as the order of encoding array
know_face_names = ["cuong","Loc"]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
# END 

# define color
red = (0,0,255)
green = (0,255,0)
blue = (255,0,0)
white = (255,255,255)
black = (0,0,0)

# shutdown function
def shutdown_server():
	func = request.environ.get('werkzeug.server.shutdown')
	if func is None:
		raise RunTimeError('Not running with Werkzeug Server')
	func()

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

# generate depth frame
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

#generate depth frame and color frame
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

#stream serial camera
def get_cam():
	# try to connect to serial camera
	try:
		cap = cv2.VideoCapture(0)
	except:
		cap = cv2.VideoCapture(3)
	ret,frame = cap.read() # try to stream frame from webcam pipeline
	width = frame.shape[1]
	height = frame.shape[0]
	zoom = 2
	dim = (width*2, height*2)
	# if take frame success
	while ret:
		ret,frame = cap.read()  
		if not ret:
			print("Connection to camera failed!")
			break
		else:
			frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
			success,buffer = cv2.imencode('.jpg',frame)
			frame = buffer.tobytes()
			
			yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#stream face-recognition on serial camera
def get_face():
	# bool var for flip frame
	process_this_frame = True
	# try to connect to serial camera # try to connect to serial camera
	try:
		cap = cv2.VideoCapture(0)
	except:
		cap = cv2.VideoCapture(3)
	ret,frame = cap.read() # try to stream frame from webcam pipeline
	width = frame.shape[1]
	height = frame.shape[0]
	zoom = 2
	dim = (width*2, height*2)
	# if take frame success
	while ret:
		ret,frame = cap.read()  
		if not ret:
			print("Connection to camera failed!")
			break
		else:
			if process_this_frame: # Only process every other frame of video to save time
				small_frame = cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
				rgb_small_frame = small_frame[:,:,::-1]
				face_locations = face_recognition.face_locations(rgb_small_frame)
				face_encodings = face_recognition.face_encodings(rgb_small_frame,face_locations)
				face_names = []
				for face_encoding in face_encodings:
					matches = face_recognition.compare_faces(known_face_encodings,face_encoding)
					name = "Unknown"
					face_distances = face_recognition.face_distance(known_face_encodings,face_encoding)
					best_match_index = np.argmin(face_distances)
					if matches[best_match_index]:
						name = know_face_names[best_match_index]
					face_names.append(name)

			process_this_frame = not process_this_frame
			for (top,right,bottom,left),name in zip(face_locations,face_names):
				top *= 4
				bottom *= 4
				right *= 4
				left *= 4
				if name == "Unknown":
					cv2.rectangle(frame,(left,top),(right,bottom),red,2)
					cv2.rectangle(frame,(left,bottom -35), (right,bottom),red,cv2.FILLED)
					cv2.putText(frame,name,(left+6,bottom-6),font,1.0,white,1)
				else:
					cv2.rectangle(frame,(left,top),(right,bottom),green,2)
					cv2.rectangle(frame,(left,bottom -35), (right,bottom),green,cv2.FILLED)
					cv2.putText(frame,name,(left+6,bottom-6),font,1.0,black,1)

			frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
			success,buffer = cv2.imencode('.jpg',frame)
			frame = buffer.tobytes()
			
			yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# HOME
@app.route("/",methods =['GET'])
def home():
    return render_template("home.html"),200

# DEPTH-CAMERA
@app.route('/color')
def colorstream():
	return Response(gen_colorframe(),mimetype = 'multipart/x-mixed-replace; boundary=frame')

@app.route('/depth')
def depthstream():
	return Response(gen_depthframe(),mimetype = 'multipart/x-mixed-replace; boundary=frame')

@app.route('/both')
def fullstream():
	return Response(gen_both(),mimetype = 'multipart/x-mixed-replace;boundary=frame')

# MANUAL CONTROL
@app.route("/manual",methods = ['GET','POST'])
def manual():
	if request.method == 'POST':
		command = request.form.get('command') # If null then not error occur
		if command:
			myrobot = Robot.query.get(1)
			myrobot.command = command
			estop = myrobot.estop # query estop value and update	
			db.session.commit()
			flash(f'Robot {command}','info')
		return  redirect(url_for('manual')),301
		myrobot = Robot.query.get(1)
		estop = myrobot.estop # query estop value and update	
		return "401,Command Not Found" #render_template('manual.html',estop),401
	myrobot = Robot.query.get(1)
	estop = myrobot.estop # query estop value and update	
	return render_template('manual.html',estop = estop),200

@app.route('/content',methods = ['POST'])
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
	return render_template('manual.html',estop = estop),200
	
@app.route('/emotion',methods = ['POST'])
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
	return render_template('manual.html',estop = estop),200
	
@app.route('/image',methods = ['POST'])
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
	return render_template('manual.html',estop = estop),200

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
		return render_template('manual.html',estop = myrobot.estop),201
	else:
		myrobot.estop = 0
		db.session.commit()
		return render_template('manual.html',estop = myrobot.estop),200

# SYSTEM
# capture color frame
@app.route("/capture_img",methods = ['POST'])
def capture_img():
	# get current frame
	ret,depth_frame,color_frame,frames = d455.get_frame()
	# get timestamp
	now = datetime.datetime.now()
	now = now.isoformat().replace(".","-")
	filename = "./imgs/" + now + ".jpg"
	# write out the frame
	cv2.imwrite(filename,color_frame)
	# update estop
	myrobot = Robot.query.get(1)
	estop = myrobot.estop # query estop value	
	return render_template('manual.html',estop = estop),200

# capture depth frame
@app.route("/capture_pointcloud",methods = ['POST'])
def capture_pointcloud():
	# get timestamp
	now = datetime.datetime.now()
	now = now.isoformat().replace(".","-")
	filename = "./pointcloud/" + now + ".ply"
	# get current frame
	ret,depth_frame,color_frame,frames = d455.get_frame()
	colorized = colorizer.process(frames)
	ply =rs.save_to_ply(filename)
	# set options to desired values, generate a textual PLY with normals (mesh is already created by default)
	ply.set_option(rs.save_to_ply.option_ply_binary,False)
	ply.set_option(rs.save_to_ply.option_ply_normals,True)
	# process your pointcloud
	ply.process(colorized)
	# update estop
	myrobot = Robot.query.get(1)
	estop = myrobot.estop # query estop value	
	return render_template('manual.html',estop = estop),200

@app.route('/shutdown',methods = ['POST'])
def shutdown():
	shutdown_server()
	return 'Server shutting down',200

# SERIAL-CAMERA
@app.route('/camera')
def camera():
	return Response(get_cam(),mimetype = 'multipart/x-mixed-replace; boundary=frame')

#FACE-RECOGNITION
@app.route('/faces')
def faces():
	return Response(get_face(),mimetype = 'multipart/x-mixed-replace; boundary=frame')


