'''
Author: locchuong
Updated: 30/8/21
Description:
    Test stream camera with opencv-contrib-python library
'''

import cv2
import argparse

# init parser
parser  = argparse.ArgumentParser(description = 'test stream camera')
# add argument to parser
parser.add_argument('-i','--id',type = int,required = True,help = 'camera number', default = 3)
# create arguments
args = parser.parse_args()


if __name__ == "__main__":

    cap = cv2.VideoCapture(args.id) # On windows cv2.CAP_DSHOW

    ret,frame = cap.read()

    while ret:
        
        ret,frame = cap.read()
        
        cv2.imshow('frame',frame)
        
        if cv2.waitKey(1) == 27:
            break 
        
    cv2.destroyAllWindows()
    cap.release()
    print('exiting...')
    exit()

