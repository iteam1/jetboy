from flask import Flask,render_template,request, Response
from flask_sqlalchemy import SQLAlchemy
import cv2 
import realsense_depth as rd
import time 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

d455 = rd.DepthCamera()

def generate_frame():
	while True:
		ret,depth_frame,color_frame = d455.get_frame()
		if not ret:
			print('Connection to camera failed!')
			break 
		else:
			success,buffer = cv2.imencode('.jpg',color_frame)
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
	print(robot)
	return render_template('base.html')

@app.route('/video')
def video():
	return Response(generate_frame(),mimetype = 'multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":

	print(d455.device)

	#app.run(debug = True,host = '0.0.0.0',port ='5000')
