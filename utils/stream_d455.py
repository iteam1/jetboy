'''
Author: locchuong
Updated: 22/6/22
Description:
    Test stream depth camera D455 with opencv-python library
'''

import cv2
import numpy as np
import realsense_depth as rd

# connect to depth camera
d455 = rd.DepthCamera() # initial depth camera object

ret,depth_frame,color_frame = d455.get_frame()

while ret:
    
    ret,depth_frame,color_frame = d455.get_frame()

    # In the heat map conversion
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_frame,alpha = 0.08),cv2.COLORMAP_JET)

    # Rendering
    images = np.hstack((color_frame,depth_colormap)) # display side by side RGB and Depth next to

    
    cv2.imshow('frame',images)
    
    if cv2.waitKey(1) == 27:
        break 
    
# release
d455.release()
cv2.destroyAllWindows()