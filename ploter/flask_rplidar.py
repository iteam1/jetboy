import cv2
import numpy as np   
from flask import Flask,render_template,Response
import matplotlib.pyplot as plt
import time
from rplidar import RPLidar 

app = Flask(__name__)

PORT_NAME = '/dev/ttyUSB0' #/dev/ttyUSB0
DMAX = 3000
IMIN = 0
IMAX = 50

def generate():

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
		success,buffer = cv2.imencode('.jpg',img)
		frame = buffer.tobytes()

		yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def base():
	return "<img src = '/plot'>"

@app.route('/plot')
def plot():
	return Response(generate(),mimetype = 'multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
	app.run(debug = True)