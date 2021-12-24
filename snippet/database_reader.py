'''
This python program continously read all value of the database print it out the screen
Run this python program on the directory ./Jetson-Nano
'''

import sqlite3
import time  

id = int(input("What is your robot's id? "))

conn = sqlite3.connect('./robot/site.db') # Create the connection to the database

c = conn.cursor() # Create the cursor for the connection

column_list = ['id','name','command','content','emotion','image','itype','estop','obs_f','obs_b','obs_l','obs_r']

print("Start reading robot id = {id}")

while True:
	c.execute(f"""
		SELECT *FROM robot WHERE id = {id} """)
	conn.commit()

	data = c.fetchone()

	message = "("
	for i in range(len(data)):
		if i == len(data) - 1: 
			message = message + column_list[i] + ' = ' + str(data[i])
		else:
			message = message + column_list[i] + ' = ' + str(data[i]) + ','

	message = message + ")" 

	print(message)

	time.sleep(0.01)

conn.close()

