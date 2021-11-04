from rplidar import RPLidar 
import numpy as np 

PORT_NAME = 'COM4'

def run():
	lidar = RPLidar(PORT_NAME)
	iterator = lidar.iter_scans()
	scan = next(iterator)
	print(scan)
	lidar.stop()
	lidar.disconnect()

while True:
	
	run()
	print("---------------------------------------------------")

lidar.stop()
lidar.disconnect()