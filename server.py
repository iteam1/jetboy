from flask import Flask,render_template,request, Response
from flask_sqlalchemy import SQLAlchemy
import cv2 
import realsense_depth as rd
import time
import numpy as np 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

# Can not detect camera after server on
d455 = rd.DepthCamera() 

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

class Robot(db.Model):
	
	id = db.Column(db.Integer,primary_key = True)
	name = db.Column(db.String(30),nullable = False,unique = True)
	command = db.Column(db.String(30),nullable = False,default = 'stop')

	def __repr__(self):
		return f"{self.name}: {self.command}"

@app.route("/",methods = ['GET'])
def base():
	return render_template('base.html')

@app.route("/command/1",methods = ['POST'])
def move():
	command = request.form.get('command')
	robot = Robot.query.get(1)
	robot.command = command 
	db.session.commit()
	#print(robot)
	return render_template('base.html')

@app.route('/colorstream')
def colorstream():
	return Response(gen_colorframe(),mimetype = 'multipart/x-mixed-replace; boundary=frame')

@app.route('/depthstream')
def depthstream():
	return Response(gen_depthframe(),mimetype= 'multipart/x-mixed-replace; boundary=frame')

@app.route('/views')
def views():
	return Response(gen_both(),mimetype= 'multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":

	app.run(host = '0.0.0.0',port ='5000')
