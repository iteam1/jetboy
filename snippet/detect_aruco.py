'''
Author: locchuong
Updated: 27/12/21
Description:
Test module aruco of opencv-contrib-python
'''
import cv2 
from cv2 import aruco
import numpy as np 

def detect_markers(img,markersize = 4, total_markers = 250, draw = True):
    '''
    Function for detect aruco marker return the bounding boxs, ids, and rejected
    '''
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # Turn the image into gray before detect
    # Define the marker size dictionary, aruco_dict = aruco.Dictionary_get(aruco.DICT_4x4_250)
    key = getattr(aruco,f"DICT_{markersize}X{markersize}_{total_markers}") # Return number 2 
    aruco_dict = aruco.Dictionary_get(key) # Get the dictionary follow constant key = aruco.DICT_4X4_250
    aruco_param = aruco.DetectorParameters_create() # Get the parameter follow the key 
    '''
        bboxs: is a tuple contain a list, each element in the list is the is a list of 4 corners 
        ex: (array([[[p1x,p1y],[p2x,p2y],[p3x,p3y],[p4x,p4y]]]), array())
		ids: is a list of the ids detected from the ids ex: [[id1],[id2],...]
		rejected: is a list of the markers rejected the same as bboxs
    '''
    bboxs,ids,rejected = aruco.detectMarkers(img_gray,aruco_dict,parameters = aruco_param)
    # if draw = True, draw the rectangle of the marker
    if draw:
        aruco.drawDetectedMarkers(img,bboxs)
    
    return bboxs,ids,rejected 

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

ret,frame =cap.read()

dimensions = frame.shape

print(f"Frame's size: height = {dimensions[0]} width = {dimensions[1]} channels = {dimensions[2]}")
    
while ret:
    
    ret,frame = cap.read()
    
    bboxs,ids,rejected = detect_markers(frame,draw = True)
    
    for i,bbox in enumerate(bboxs):
        
        frame =cv2.circle(frame,tuple(bbox[0][0].astype(int)),5,(0,255,0),-1)
        
        cv2.putText(frame,str(ids[i]),tuple(bbox[0][0].astype(int)),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)
        
    cv2.imshow('frame',frame)
        
    if cv2.waitKey(1) == 27:
        break 
    
cv2.destroyAllWindows()
cap.release()
    
