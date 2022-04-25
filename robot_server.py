'''
Author: locchuong
Updated: 27/12/21
Description:
	Run the server.py to create a local to interface with the robot
'''
# This is the main server for control robot
from robot import app 

if __name__ == "__main__":
	app.run(host = '0.0.0.0', port = 5000)
