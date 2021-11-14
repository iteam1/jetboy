import random
import cv2
import numpy as np   
from flask import Flask,render_template,Response
import matplotlib.pyplot as plt
import time 

app = Flask(__name__)

s = []

def generate():
	while True:
		s.append(random.randint(3,9))
		fig = plt.figure()
		ax = fig.subplots()
		ax.plot(s)
		#ax.plot([1,2,3,5,7])
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