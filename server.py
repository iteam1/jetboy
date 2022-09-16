'''
Author: locchuong
Updated: 22/6/22
Description:
	Run the server.py to create a local to interface with the robot
'''
# This is the main server for control robot
from robot import app
from robot import d455

if __name__ == "__main__":

	print('[MISSION3]: server is running...')

	app.run(host = '0.0.0.0', port = 5000) #loop over

	print('[MISSION3]: server shutdowned!')
	
	d455.release()

	print('[MISSION3]: camera released!')

	exit()
