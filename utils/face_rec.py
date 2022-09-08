'''
Author: locchuong
Updated: 8/9/22
Description:
    Test face recognition realtime
'''

import cv2
import argparse
# import face_recognition

# init parser
parser  = argparse.ArgumentParser(description = 'test stream camera')
# add argument to parser
parser.add_argument('-i','--id',type = int,required = True,help = 'camera number', default = 0)
parser.add_argument('-w','--windows',action = 'store_true',help = 'check os sytem windows or linux,etc')
# create arguments
args = parser.parse_args()

if __name__ == "__main__":

    if args.windows:
        cap = cv2.VideoCapture(args.id,cv2.CAP_DSHOW) # On windows cv2.CAP_DSHOW
    else:
        cap = cv2.VideoCapture(args.id)

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

