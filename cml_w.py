import time 
import sqlite3 

if __name__ == "__main__":

	conn = sqlite3.connect("site.db")

	c = conn.cursor()

	print("Connected to Robot's database via Command Line!")

	id = int(input('Enter robot ID: '))

	while True:

		command = input("Enter your command: ")

		if command == "q":
			print("Close the connection")
			break

		elif command == "x":
			c.execute(f"UPDATE robot SET command = 'kill' WHERE id = {id}")
			c.execute(f"SELECT *FROM robot WHERE id = {id}")
			print(c.fetchall())
			conn.commit()
			time.sleep(1) #delay for command exit in reader
			print("Stop motor & Clean up")
			break

		elif command == "t":
			c.execute(f"UPDATE robot SET command = 'stop' WHERE id = {id}")
			c.execute(f"SELECT *FROM robot WHERE id = {id}")
			print(c.fetchall())
			conn.commit()

		elif command == "w":
			c.execute(f"UPDATE robot SET command = 'forward' WHERE id = {id}")
			c.execute(f"SELECT *FROM robot WHERE id = {id}")
			print(c.fetchall())
			conn.commit()


		elif command == "s":
			c.execute(f"UPDATE robot SET command = 'backward' WHERE id = {id}")
			c.execute(f"SELECT *FROM robot WHERE id = {id}")
			print(c.fetchall())
			conn.commit()

		elif command == "a":
			c.execute(f"UPDATE robot SET command = 'turnleft' WHERE id = {id}")
			c.execute(f"SELECT *FROM robot WHERE id = {id}")
			print(c.fetchall())
			conn.commit()

		elif command == "d":
			c.execute(f"UPDATE robot SET command = 'turnright' WHERE id = {id}")
			c.execute(f"SELECT *FROM robot WHERE id = {id}")
			print(c.fetchall())
			conn.commit()

		else:
			print("Command does not Exist!")
			pass

	c.execute(f"UPDATE robot SET command = 'stop' WHERE id = {id}")
	c.execute(f"SELECT *FROM robot WHERE id = {id}")
	print(c.fetchall())
	conn.commit()
	conn.close()

	print("Exit cml")














