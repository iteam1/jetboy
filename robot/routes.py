from flask import render_template,request,Response,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import cv2 
import realsense_depth as rd
import numpy as np

def gen_colorframe():
	while True:
		ret,depth_frame,color_frame = d455.get_frame()
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
		ret,depth_frame,color_frame = d455.get_frame()

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
		ret,depth_frame,color_frame = d455.get_frame()

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

@app.route("/helm",methods = ['GET','POST'])
def helm():
	if request.method == 'POST':
		command = request.form.get('command')
		face = request.form.get.get('face')
		if command:
			robot = Robot.query.get(1)
			robot.command = command 
			db.session.commit()
			flash(f'Robot {command}','info')
		if face:
			robot = Robot.query,get(1)
			robot.face = face 
			db.session.commit()
		return  redirect(url_for('helm'))

	return render_template('helm.html')


@app.route('/color')
def colorstream():
	return Response(gen_colorframe(),mimetype = 'multipart/x-mixed-replace; boundary=frame')

@app.route('/depth')
def depthstream():
	return Response(gen_depthframe(),mimetype = 'multipart/x-mixed-replace; boundary=frame')


@app.route('/content',methods =['GET','POST'])
def content():
	if request.method == 'POST':
		content = request.form.get('content')
		showman = Showman.query.get(1)
		showman.itype = 'info'
		showman.content = content
		db.session.commit()
		return render_template('helm.html')
	return render_template('helm.html')

@app.route('/emotion',methods =['GET','POST'])
def emotion():
	if request.method == 'POST':
		emotion = request.form.get('emotion')
		showman = Showman.query.get(1)
		showman.itype = 'emo'
		showman.emotion = emotion
		db.session.commit()
		return render_template('helm.html')
	return render_template('helm.html')

@app.route('/image',methods =['GET','POST'])
def image():
	if request.method == 'POST':
		image = request.form.get('image')
		showman = Showman.query.get(1)
		showman.itype = 'img'
		showman.image = image
		db.session.commit()
		return render_template('helm.html')
	return render_template('helm.html')
