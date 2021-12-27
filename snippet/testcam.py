'''
Author: locchuong
Updated: 27/12/21
Description:
Test stream camera with opencv-contrib-python library
'''

import cv2

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

ret,frame = cap.read()

while ret:
    
    ret,frame = cap.read()
    
    cv2.imshow('frame',frame)
    
    if cv2.waitKey(1) == 27:
        break 
    
cv2.destroyAllWindows()

cap.release()