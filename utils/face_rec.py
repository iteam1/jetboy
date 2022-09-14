'''
Author: locchuong
Updated: 8/9/22
Description:
    Test face recognition realtime
'''

import cv2
import argparse
import face_recognition
import numpy as np

# init parser
parser  = argparse.ArgumentParser(description = 'test stream camera')
# add argument to parser
parser.add_argument('-i','--id',type = int,required = True,help = 'camera number', default = 0)
parser.add_argument('-w','--windows',action = 'store_true',help = 'check os sytem windows or linux,etc')
# create arguments
args = parser.parse_args()

# font
font = cv2.FONT_HERSHEY_DUPLEX # cv2.FONT_HERSHEY_SIMPLEX

# load a sample picture and learn how to recognize it.
cuong_image = face_recognition.load_image_file('./faces/cuong.png')
cuong_face_encoding = face_recognition.face_encodings(cuong_image)[0]

loc_image = face_recognition.load_image_file('./faces/loc.png')
loc_face_encoding = face_recognition.face_encodings(loc_image)[0]

# create arrays of know face encodings and their names
known_face_encodings = [cuong_face_encoding,loc_face_encoding]

# create a list of names as the order of encoding array
known_face_names = ["cuong","Loc"]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

if __name__ == "__main__":

    # get a reference to webcam
    if args.windows:
        cap = cv2.VideoCapture(args.id,cv2.CAP_DSHOW) # On windows cv2.CAP_DSHOW
    else:
        cap = cv2.VideoCapture(args.id)
    # try to stream frame from webcam pipeline
    ret,frame = cap.read()

    while ret:
        
        ret,frame = cap.read()

        # Only process every other frame of video to save time
        if process_this_frame:
            
            # Resize frame to 1/4size for faster face recogintion processing
            small_frame = cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
            
            # Convert the image from BGR color (Which OpenCV uses) to RGB color (which regnition uses)
            rgb_small_frame = small_frame[:,:,::-1]
            
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame,face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings,face_encoding)
                # At the first name is
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smalllest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings,face_encoding)
                best_match_index = np.argmin(face_distances)
                # if the min distance index is get true in matches
                if matches[best_match_index]:
                    name = know_face_names[best_match_index]
                face_names.append(name)

        process_this_frame = not process_this_frame # revert bit process_this_frame for the next frame

        # Display the results
        for (top,right,bottom,left),name in zip(face_locations,face_names):
            # scale back up locations since the frame we detected in was scaled tp 1/4 size
            top *= 4
            bottom *= 4
            right *= 4
            left *= 4

            # draw a box around the face
            cv2.rectangle(frame,(left,top),(right,bottom),(0,0,255),2)

            # Draw a label with a name below the face
            cv2.rectangle(frame,(left,bottom -35), (right,bottom), (0,0,255),cv2.FILLED)
            cv2.putText(frame,name,(left+6,bottom-6),font,1.0,(255,255,255),1)


        cv2.imshow('frame',frame)
        
        # Hit 'q' on the keyboard to quit!
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

        if cv2.waitKey(1) == 27:
            break 
        
    cv2.destroyAllWindows()
    cap.release()
    print('exiting...')
    exit()

