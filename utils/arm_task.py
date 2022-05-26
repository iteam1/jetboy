import serial
from serial.tools import list_ports
import time 

# check all impossible port and list it
ports = list_ports.comports()
for port,desc,hwid in sorted(ports):
	print("{}: {} [{}]".format(port,desc,hwid))

port  = input('Enter your port name: ')
arduino = serial.Serial(port,baudrate = 9600,timeout = 0.1)

def grip_cup():
	x = "180,60,90,90,20,1" + "a"
	arduino.write(x.encode())
	time.sleep(4)
	x = "180,60,180,90,20,1" + "a"
	arduino.write(x.encode())
	time.sleep(4)
	x = "180,40,180,90,20,1" + "a"
	arduino.write(x.encode())
	time.sleep(4)
	x = "180,40,180,90,120,1" + "a"
	arduino.write(x.encode())
	time.sleep(4)
	x = "180,90,90,90,120,1" + "a"
	arduino.write(x.encode())
	time.sleep(4)
	x = "180,90,90,90,90,1" + "a"
	arduino.write(x.encode())
	time.sleep(4)

if __name__ == "__main__":
	print('wait until robot go to the eady position...')
	while True:
		x = input('Enter the framework: ')
		# break out of the while loop if you press 'x'
		if x == 'x':
			break
		elif x == 'cup':
			grip_cup()
		x = x + "a" # read the frame until a
		print(x)
		#arduino.write(bytes(x,'utf-8'))
		arduino.write(x.encode())

	# go home
	x = "180,90,90,90,90,1" + "a"
	arduino.write(x.encode())
	time.sleep(1)
	x = "90,90,90,90,90,1" + "a"
	arduino.write(x.encode())
	time.sleep(1)
	x = "90,20,90,90,90,1" + "a"
	arduino.write(x.encode())
	time.sleep(1)
	# close the connection
	arduino.close()