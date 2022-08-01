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
from robot.pyrealsense2 import pyrealsense2 as rs
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
	return render_template('manual.html',estop = estop)

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
	return render_template('manual.html',estop = estop)