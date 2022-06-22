'''
Author: locchuong
Updated: 22/6/22
Description:
	This python program continously read all value of the database print it out the screen
	Run this python program on the directory ./Jetson-Nano
'''

import os 
import time
import sqlite3
import argparse
from datetime import datetime

# init parser
parser = argparse.ArgumentParser(description = ' Query database and print it out continously')
# add argument to parser
parser.add_argument('-n','--id', type = int, help = 'robot id', required = True)
parser.add_argument('-t','--time',type = float,help = 'timedelay display', default = 0.1)
# create arguments
args = parser.parse_args()

# connect to database sqlite3
conn = sqlite3.connect('./robot/site.db') # Create the connection to the database
c = conn.cursor() # Create the cursor for the connection
print('database connected!')
# check database id
# id = int(input("What is your robot's id? "))
# what column that you want to read
column_list = ['id','name','command','content','emotion','image','itype','estop','obs_f','obs_b','obs_l','obs_r']
print("Start reading robot id = {id}")

if __name__ == "__main__":
	while True:
		# query database
		c.execute(f"""
			SELECT *FROM robot WHERE id = {args.id} 
			""")
		conn.commit()
		# get data follow your query
		data = c.fetchone() # a tuple
		# make the message
		message = str(datetime.now()) + "\n{\n" 
		for i in range(len(data)):
			# if you to the last of message then don't have to add comma
			if i == len(data) - 1: 
				message = message + column_list[i] + ' = ' + str(data[i])
			else:
				message = message + column_list[i] + ' = ' + str(data[i]) + ', \n'
		message = message + "\n}\n" 
		# print out the message
		print(message)
		# delay
		time.sleep(0.1)
		# clear the output
		os.system('clear')

	conn.close()

