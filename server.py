from flask import Flask,render_template,request,Response,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import cv2 
import realsense_depth as rd
import numpy as np 
from rplidar import RPLidar
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the random string'    
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

# Can not detect camera after server on
d455 = rd.DepthCamera() 

# RPlidar
PORT_NAME = '/dev/ttyUSB0' 
DMAX = 3000
IMIN = 0
IMAX = 50

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

def gen_camlidar():

	def update_line(iterator, line):
	    scan    = next(iterator)
	    #print(scan)
	    offsets = np.array([(np.radians(meas[1]), meas[2]) for meas in scan])
	    line.set_offsets(offsets)
	    intens  = np.array([meas[0] for meas in scan])
	    line.set_array(intens)
	    return line

	fig   = plt.figure()
	ax    = plt.subplot(111, projection='polar')
	line  = ax.scatter([0, 0], [0, 0], s=5, c=[IMIN, IMAX],cmap=plt.cm.Reds_r, lw=2)

	ax.set_rmax(DMAX)
	ax.grid(True)

	while True:

		lidar = RPLidar(PORT_NAME)

		iterator = lidar.iter_scans()

		line = update_line(iterator,line)

		lidar.stop()
		lidar.disconnect()

		fig.canvas.draw()

		# convert canvas to image
		img = np.fromstring(fig.canvas.tostring_rgb(),dtype=np.uint8,sep='')
		img  = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
		
		# img is rgb, convert to opencv's default bgr
		img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)

		ret,depth_frame,color_frame = d455.get_frame()

		images = np.hstack((color_frame,img)) # display side by side RGB and Depth next to

		if not ret:
			print("Connection to camera failed!")
			break
		else:
			success,buffer = cv2.imencode('.jpg',images)
			frame = buffer.tobytes()

			yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
		# success,buffer = cv2.imencode('.jpg',img)
		# frame = buffer.tobytes()

		# yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

class Robot(db.Model):
	
	id = db.Column(db.Integer,primary_key = True)
	name = db.Column(db.String(30),nullable = False,unique = True)
	command = db.Column(db.String(30),nullable = False,default = 'stop')

	def __repr__(self):
		return f"{self.name}: {self.command}"

@app.route("/",methods = ['GET','POST'])
def base():
	if request.method == 'POST':
		command = request.form.get('command')
		robot = Robot.query.get(1)
		robot.command = command 
		db.session.commit()
		flash(f'Robot {command}','info')
		return  redirect(url_for('base'))#render_template('base.html')

	return render_template('base.html')


@app.route('/colorstream')
def colorstream():
	return Response(gen_colorframe(),mimetype = 'multipart/x-mixed-replace; boundary=frame')

@app.route('/depthstream')
def depthstream():
	return Response(gen_depthframe(),mimetype= 'multipart/x-mixed-replace; boundary=frame')

@app.route('/views')
def views():
	return Response(gen_camlidar(),mimetype= 'multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":

	app.run(host = '0.0.0.0',port ='5000')
