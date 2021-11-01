from controller import MotorController
import RPi.GPIO
import sqlite3 
import time 

if __name__ == "__main__":

	controller = MotorController()

	conn = sqlite3.connect("site.db")

	c = conn.cursor()

	print("Connected to Robot's database via Command Line!")

	id = int(input('Enter robot ID: '))

	print("Robot is running...")

	while True:

		c.execute(f"SELECT *FROM robot WHERE id = {id}")
		#print(c.fetchone()[2])
		command = c.fetchone()[2]
		conn.commit()

		if command == "kill":
			print("Stop motor & Clean up")
			break

		elif command == "stop":
			controller.stop()

		elif command == "forward":
			controller.forward()

		elif command == "backward":
			controller.backward()

		elif command == "turnleft":
			controller.turnleft()

		elif command == "turnright":
			controller.turnright()

		else:
			print("Command does not Exist!")
			pass

	controller.stop()
	RPi.GPIO.cleanup()
	conn.close()
	print("Exit cml")











