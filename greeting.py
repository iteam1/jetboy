'''
Author: locchuong
Updated: 14/9/22
Description:
	This is the first mission of robot intergate A.I,
	Greeting people, there are  
	(^ ^) = known-face
	(o o) = unknown-face
'''
import os
import cv2
import argparse
import face_recognition
import numpy as np

# define color
red = (0,0,255)
green = (0,255,0)
blue = (255,0,0)
white = (255,255,255)
black = (0,0,0)

# font
font = cv2.FONT_HERSHEY_DUPLEX # cv2.FONT_HERSHEY_SIMPLEX

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
known_face_encodings = []
known_face_names = []

def read_faces():
	files = os.listdir("./faces")
	for file in files:
		file = file.split(".")
		file_name = file[0]
		file_format = file[-1]
		if file_format in ["jpg","jpeg","png"]:
			image_file = os.path.join("./faces/",file_name+"."+file_format)
			face = face_recognition.load_image_file(image_file)
			encoding = face_recognition.face_encodings(face)[0] # return a list, take the first element
			known_face_names.append(file_name)
			known_face_encodings.append(encoding)
	return known_face_names,known_face_encodings

def main():

	process_this_frame = True

	print("MISSION 4 reading faces")
	known_face_names,known_face_encodings = read_faces()

	cap = cv2.VideoCapture(3)
	
	ret,frame = cap.read()

	while ret:

		ret,frame = cap.read()

		if process_this_frame:

			small_frame = cv2.resize(frame,(0,0),fx=0.25,fy=0.25)

			rgb_small_frame = small_frame[:,:,::-1]

			face_locations = face_recognition.face_locations(rgb_small_frame)

			face_encodings = face_recognition.face_encodings(rgb_small_frame,face_locations)

			face_names = []

			for face_encoding in face_encodings:

				matches = face_recognition.compare_faces(known_face_encodings,face_encoding)

				name = "Unknown"

				face_distances = face_recognition.face_distance(known_face_encodings,face_encoding)

				best_match_index = np.argmin(face_distances)

				if matches[best_match_index]:
					name = known_face_names[best_match_index]

				face_names.append(name)

		process_this_frame = not process_this_frame 

		for (top,right,bottom,left),name in zip(face_locations,face_names):
			top *= 4
			bottom *= 4
			right *= 4
			left *= 4

			if name == "Unknown":
				cv2.rectangle(frame,(left,top),(right,bottom),red,2)
				cv2.rectangle(frame,(left,bottom -35), (right,bottom),red,cv2.FILLED)
				cv2.putText(frame,name,(left+6,bottom-6),font,1.0,white,1)
			else:
				cv2.rectangle(frame,(left,top),(right,bottom),green,2)
				cv2.rectangle(frame,(left,bottom -35), (right,bottom),green,cv2.FILLED)
				cv2.putText(frame,name,(left+6,bottom-6),font,1.0,black,1)

		cv2.imshow('frame',frame)

		if cv2.waitKey(1) == 27:
			break 

	cv2.destroyAllWindows()
	cap.release()
	print('exiting...')
	exit()

if __name__ == "__main__":
	main()