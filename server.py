# This is the main server for control robot
from flask import Flask,render_template,request,Response,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import cv2 
import realsense_depth as rd
import numpy as np
#import webbrowser  

app = Flask(__name__)
app.config['SECRET_KEY'] = '3b9fed3b85a77047fc95896683ee6713'    
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

# Can not detect camera after server on
d455 = rd.DepthCamera() 

# Generate colorframe
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

class Robot(db.Model):
	
	id = db.Column(db.Integer,primary_key = True)
	name = db.Column(db.String(30),nullable = False,unique = True)
	command = db.Column(db.String(30),nullable = False,default = 'stop')
	face = db.Column(db.Integer,nullable = False,default =0)

	def __repr__(self):
		return f"{self.name}: {self.command}"

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

if __name__ == "__main__":
	# This comment line come from dell linux
    # webbrowser.open(url = '0.0.0.0:5000')
    app.run(host = '0.0.0.0',port ='5000')
