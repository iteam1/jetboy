'''
Author: locchuong
Date: 26/5/2022
Descript:
	Finding aruco target, display on screen:
		- ID
		- position of x,y
		- depth
		- square area
'''
import cv2  
import cv2.aruco as aruco 
import numpy as np
import realsense_depth as rd # pyrealsense2 package is already in snippet
import math

# define color
red = (0,0,255)
green = (0,255,0)
blue = (255,0,0)
center_point = (320,240)
vdim = 40
hdim = 30

def check_LR(center_point,current_point,x_distance):
	'''
	Check the position of target
	Arguments:
		center_point --- center point on the screen
		current_point --- current position of the aruco
		x_distance --- the acceptable distance 
	Return:
		(string) left right or center
	'''
	if current_point[0] < center_point[0] - x_distance:
		return 'Left'
	elif current_point[0] > center_point[0] + x_distance:
		return 'Right'
	elif (current_point[0] >= center_point[0] - x_distance) & (current_point[0] <= center_point[0] + x_distance):
		return 'Center'

def check_TB(center_point,current_point,y_distance):
	'''
	Check the position of target
	Arguments:
		center_point --- center point on the screen
		current_point --- current position of the aruco
		y_distance --- the acceptable distance 
	Return:
		(string) top bottom or center
	'''
	if current_point[1] < center_point[1] - y_distance:
		return 'Top'
	elif current_point[1] > center_point[1] + y_distance:
		return 'Bottom'
	elif (current_point[1] >= center_point[1] - y_distance) & (current_point[1] <= center_point[1] + y_distance):
		return 'Center'

def calc_S(bbox):
	'''
	calculate the square area of the aruco
	'''
	top_left  = bbox[0][0] # top left corner (x,y)
	top_right = bbox[0][1] # top right corner (x,y)
	bottom_right = bbox[0][2] # bottom left corner (x,y)
	bottom_left = bbox[0][3] # bottom right corner (x,y)
	l = math.sqrt((top_right[0]-bottom_left[0])**2+(top_right[1]-bottom_left[1])**2) # the distane between of top-right and bottom-left (x,y)
	m = (top_right[1] - bottom_left[1])/(top_right[0]-bottom_left[0])
	b = top_right[1] - m * top_right[0]
	h1 = abs(m * top_left[0] - top_left[1] + b)/math.sqrt(m**2 + 1)
	h2 = abs(m * bottom_right[0] - bottom_right[1] + b)/math.sqrt(m**2 + 1)

	return round((0.5*l*h1 + 0.5*l*h2),2)

def find_aruco_markers(img,depth,marker_size = 4,total_markers = 250,draw  = True):
	'''
	Find aruco in frame
	Arguments:
		img --- color frame of image
		marker_size --- size of marker default = 4 (4,5,6)
		total_markers --- total markers in frame
		draw --- option to draw marker on the screen
	'''
	centroids = [] # list of centroids marker
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # convert your image to gray color
	key = getattr(aruco,f'DICT_{marker_size}X{marker_size}_{total_markers}')
	aruco_dict = aruco.Dictionary_get(key) 
	aruco_param = aruco.DetectorParameters_create()
	bboxs,ids,rejected = aruco.detectMarkers(gray,aruco_dict, parameters = aruco_param) # detect aruco targets
	
	# find the centroids list, if bboxs empty, this for loop does not break program
	for i,bbox in enumerate(bboxs):
		# get the centroid
		centroid = np.mean(bbox,axis = 1).astype('int')
		centroid = tuple(centroid[0]) # centroid.shape = (1,1)
		centroids.append(centroid)
		#find the anchor point for display infomation
		pt = bbox[0][1].astype('int') # bbox.shape  = (1,4,2) the top_right point, this is one of 4 aruco's corners 0 = top-left, 1 = top-right, 2 = bottom-right,3 = bottom-left
		# draw the infomation on the screen
		# cv2.circle(img,(pt[0],pt[1]),10,red,-1) # center point
		# get distance of this point
		distance = depth[pt[1],pt[0]] #y,x
		# get square area of the aruco
		S = calc_S(bbox)
		# display it on screen
		cv2.putText(img, f'{distance}',(pt[0],pt[1]-15), cv2.FONT_HERSHEY_SIMPLEX,0.5, green, 1, cv2.LINE_AA)
		cv2.putText(img, f'{ids[i]}',(pt[0],pt[1]), cv2.FONT_HERSHEY_SIMPLEX,0.5, green, 1, cv2.LINE_AA)
		cv2.putText(img, f'{centroid}',(pt[0],pt[1]+15), cv2.FONT_HERSHEY_SIMPLEX,0.5, green, 1, cv2.LINE_AA)
		cv2.putText(img, f'{S}',(pt[0],pt[1]+25), cv2.FONT_HERSHEY_SIMPLEX,1,red, 1, cv2.LINE_AA)
		cv2.circle(img,centroid,3,green,-1) # center point
		# if the current aruco get id equal to your specification
		if ids[i] == 7:
			cv2.putText(img, f'ID7: {distance} {check_LR(center_point,centroid,vdim)} {check_TB(center_point,centroid,hdim)}',(50,25), cv2.FONT_HERSHEY_SIMPLEX,1, green, 1, cv2.LINE_AA)
			cv2.line(img,center_point,centroid,red,2)

	if draw:
		aruco.drawDetectedMarkers(img,bboxs)

d455 = rd.DepthCamera() # initial depth camera
# Check the connection and try to get data
ret,depth_frame,color_frame = d455.get_frame()

if __name__ == '__main__':
	while ret:
		ret,depth_frame,color_frame = d455.get_frame()
		colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_frame,alpha = 0.08),cv2.COLORMAP_JET)
		#print(depth_frame.shape)
		
		# find aruco in frame
		find_aruco_markers(color_frame,depth_frame)
		
		# draw info on color_frame
		cv2.circle(color_frame,center_point,10,blue,2) # center point
		cv2.line(color_frame,(320,220),(320,260),blue,2) # vertical line
		cv2.line(color_frame,(300,240),(340,240),blue,2) # horizontal line
		cv2.line(color_frame,(320-vdim,0),(320-vdim,480),blue,2) # vertical frontline left
		cv2.line(color_frame,(320+vdim,0),(320+vdim,480),blue,2) # vertical frontline right
		cv2.line(color_frame,(0,240-hdim),(640,240-hdim),blue,2) # horizontal frontline top
		cv2.line(color_frame,(0,240+hdim),(640,240+hdim),blue,2) # horizontal frontline top

		# Display color frame
		cv2.imshow('color_frame',color_frame)
		cv2.imshow('depth_frame',colormap)

		if cv2.waitKey(1) == 27:
			break 

	d455.release()
	cv2.destroyAllWindows()