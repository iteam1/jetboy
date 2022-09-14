'''
Author: locchuong
Updated: 14/9/22
Description:
	This is the first mission of robot intergate A.I,
	Greeting people, there are  
	(^ ^) = known-face
	(o o) = unknown-face
'''
# FACE RECOGNTION
import os
import cv2
import argparse
import face_recognition
import numpy as np
import sqlite3 

# font
font = cv2.FONT_HERSHEY_DUPLEX # cv2.FONT_HERSHEY_SIMPLEX
zoom = 2 # zoom frame
# define color
red = (0,0,255)
green = (0,255,0)
blue = (255,0,0)
white = (255,255,255)
black = (0,0,0)

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
known_face_encodings = []
known_face_names = []

# count iteration
count = 0

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

# Create the connection to the database and the cursor
conn = sqlite3.connect("./robot/site.db") # ./Jetson-Nano you must define this conn before add in into default keyword arg

# Create a api object for connecting to database and modify it
class api_db():

	def __init__(self,conn =conn):
		self.conn = conn # the connection to site database

	def read_emotion(self):
		'''
		This function read the command value in database and return it
		'''
		c = self.conn.cursor()
		c.execute(f"SELECT *FROM robot WHERE id = 1")
		data = c.fetchone()
		emotion = data[4]
		itype = data[6]
		self.conn.commit()
		return emotion,itype

	def write_emotion(self,emotion='neutral'):
		'''
		This function for write the emotion to database, must set itype = emo
		'''
		c = self.conn.cursor()
		c.execute("""
			UPDATE robot
			SET itype = ?, emotion = ?
			WHERE id = 1
			""",('emo',emotion))
		self.conn.commit()

	def kill_gpio(self):
		'''
		This function for close gpio program
		'''
		c = self.conn.cursor()
		c.execute(f"""
			UPDATE robot
			SET command = 'kill'
			WHERE id = 1
			""")
		self.conn.commit()

if __name__ == "__main__":

	# init emoled database api object
	api = api_db()

	emotion,itype = api.read_emotion()

	print(f"[MISSION4]: {itype} {emotion}")

	# flip bool for processing frame
	process_this_frame = True

	print("[MISSION4]: reading faces...")
	known_face_names,known_face_encodings = read_faces()

	cap = cv2.VideoCapture(3)
	ret,frame = cap.read()

	width = frame.shape[1]
	height = frame.shape[0]
	dim = (width*2, height*2)

	if not ret:
		print("[MISSION4]: FAILED (Can not connect to camera)")

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
				api.write_emotion(emotion="angry")
			else:
				cv2.rectangle(frame,(left,top),(right,bottom),green,2)
				cv2.rectangle(frame,(left,bottom -35), (right,bottom),green,cv2.FILLED)
				cv2.putText(frame,name,(left+6,bottom-6),font,1.0,black,1)
				api.write_emotion(emotion="smile")

		frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
		cv2.imshow('frame',frame)

		# read emotion
		emotion,itype = api.read_emotion()

		if count % 10 ==0 and emotion != "neutral":
			count = 0
			api.write_emotion(emotion="neutral")

		count +=1
		#print(count)
		
		if cv2.waitKey(1) == 27:
			break

	cv2.destroyAllWindows()
	cap.release()
	api.kill_gpio()
	print("[MISSION4]: DONE")
	exit()