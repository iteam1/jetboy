'''
This program will create a new robot database, then flask server will connect to this database will a robot model

1/ id: is the robot id (primary key)
2/ name: robot's name

# Control robot's action

3/ command: This one will control the robot's action
	value: 
		- stop: robot will stop moving
		- forward: robot will moving forward
		- backward: robot will moving backward
		- turnleft: robot will turn left
		- turnright: robot will turn right

	...


# Control robot's GUI display on the screen

4/ content: the sentence content will display on the robot screen for TEXT,WORDS DISPLAY
5/ emotion: the name of gif image will display on the robot screen for GIF,EMOTION DISPLAY
6/ image: the name of the image will display on the robot screen for IMAGE DISPLAY
7/ itype: the content's type will display on the robot
	value:
		- info: display content on the screen
		- emo: display emotion or gif on the screen
		- img: display the image on the screen
'''

import sqlite3 

conn = sqlite3.connect("site.db")

c = conn.cursor()

c.execute("""
	CREATE TABLE robot(
	id INTEGER PRIMARY KEY,
	name TEXT,
	command TEXT,
	content TEXT,
	emotion TEXT,
	image TEXT,
	itype TEXT
	)
	""")

conn.commit()

print('Database created!')

conn.close()