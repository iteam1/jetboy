## Hardware
Jetson-nano B01 

## Features
- Control manually via webserver
- Display GIF, images, words on screen
- 4 sensors HC-SR04 for detect obstacles Best range: 0-100cm, sweep angle: 15 degrees, 44kHz 
- RPlidar A1 scanning
- Streaming depth camera realsense D455
- Detect object with GPU on Jetson Nano board via Yolo v3 model

## Developing
- Follow a path automatically
- Do a specific task

## Required libraries
The library with have * mark meaning you can not install it with command `pip install -r requirements.txt`, (*) meaning can not install this library normally
- jetson.GPIO (*This libary is built-in jetson-nano board or rasberry pi board, and just can run on this hardware)
- flask `pip3 install flask`
- flask_sqlachemy `pip3 install flask_sqlalchemy`
- sqlite3  (builtin lib)
- tkinter (builtin lib)
- pyrealsense2  (*)
- opencv-contrib-python (*)
- os (builtin lib)
- pynput `pip3 install pynput`
    
# Run all program via bash script

`bash start.sh`

# Run custom program

- Run gpio controller `python3 robot_gpio.py`

- Run gui controller `python3 robot_gui.py`

- Run webserver `python3 robot_server.py`

# Generate database

`python3 gendata.py`

Open terminal:

	```
	from robot import db
	from robot.models import Robot
	robot = Robot()
	db.add(robot)
	db.commit()
	```