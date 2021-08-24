from flask import Flask, render_template, Response
import cv2
from realsense_camera import *
from mask_rcnn import *

# Load Realsense camera
rs = RealsenseCamera()
mrcnn = MaskRCNN()

app = Flask(__name__)

@app.route('/view')
def normal_view():
	return render_template('page_view.html')

def normal_view():
	while True:
		
		# Get frame in real time from Realsense camera
		ret, bgr_frame, depth_frame = rs.get_frame_stream()

		if not ret:
			print('Connection failed!')
			break
		else:
			success,buffer =  cv2.imencode('.jpg',bgr_frame)
			frame = buffer.tobytes()

			yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/normal_rep')
def normal_stream():
	return Response(normal_view(),mimetype = 'multipart/x-mixed-replace; boundary=frame')


@app.route('/detect')
def rcnn_view():
	return render_template('page_detect.html')

def rcnn_frame():
	while True:
		
		# Get frame in real time from Realsense camera
		ret, bgr_frame, depth_frame = rs.get_frame_stream()

		# Get object mask
		boxes, classes, contours, centers = mrcnn.detect_objects_mask(bgr_frame)

		# Draw object mask
		bgr_frame = mrcnn.draw_object_mask(bgr_frame)

		# Show depth info of the objects
		mrcnn.draw_object_info(bgr_frame, depth_frame)

		if not ret:
			print('Connection failed!')
			break
		else:
			success,buffer =  cv2.imencode('.jpg',bgr_frame)
			frame = buffer.tobytes()

			yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/rcnn_rep')
def rcnn_stream():
	return Response(rcnn_frame(),mimetype = 'multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
	app.run(host = '192.168.1.9', port = 5000)





