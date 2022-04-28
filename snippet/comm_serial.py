import serial
import time 

arduino = serial.Serial('COM4',baudrate = 9600,timeout = 0.1)

if __name__ == "__main__":
	while True:
		x = input('Enter the framework: ')
		#arduino.write(bytes(x,'utf-8'))
		arduino.write(x.encode())