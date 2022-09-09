### initialize-guide

**step1**: install a code-editor `bash sublime-text.sh`.

**step2**: install `python3-pip` package: `sudo apt-get update & sudo apt-get install python3-pip`.

**step3**: install python packages virtual enviroment `pip3 install virtualenv`.

**step4**: install pyrealsense for using D455 depth camera `bash pyrealsense.sh`. pyrealsense can not install normally by `pip3`

**step5**: install opencv `sudo apt-get install python3-opencv` (stable version)

**step6**: install face-recognition

     sudo apt-get install libboost-all-dev
     sudo apt-get install libgtk-3-dev
     sudo apt-get install build-essential cmake
     sudo apt-get update 
     sudo apt-get install cmake
     sudo apt-get install scikit-image 
     pip3 install scikit-learn 

      pip3 install numpy scikit-learn cmake
      pip3 install dlib
      pip3 install face_recognition


**step7**: install the other required packages by in [requirements.txt](/init/requirements.txt) `pip3 install -r requirements.txt`

these packages can be install normally by `pip3 install [package_name]`, [requirements.txt](/init/requirements.txt) contain the main packages and their dependencies, bellow is main packages you can install them manually by `pip3 install [package_name]`.

     flask
     flask_sqlalchemy
     sqlite3
     numpy
     pyserial

- export packages into requirements.txt: `pip3 freeze > requirements.txt`

*Notes:* All packages,libraries and dependencies must be install in gobal. `RPi.GPIO` is build-in package and only can be install on embedded-hardwares like jetson-board or raspberry-board.

**bash-scripts table**

|No|Script|Description|Comment|
|---|---|---|---|
|01|[sublime-text.sh](/init/sublime-text.sh)|install code editor sublime-text|*required*|
|02|[pyrealsense.sh](/init/pyrealsense.sh)|install pyrealsense python library|*required*|
|03|[opencv-contrib.sh](/init/opencv-contrib.sh)|install opencv-contrib version for jetson-nano, build from source||
|04|[tensorflow.sh](/init/tensorflow.sh)|install tensorflow for jetson-nano||
______

#### init database

the database `sqlite3` is already there in the repo, but if you lost it, in `/utils` folder Run python script for generate a sqlite database: `python3 robot/gendata.py`, this command will create a datbase and a table. Then open terminal and add a row into that table:

	from robot import db
	from robot.models import Robot
	robot = Robot()
	db.session.add(robot)
	db.session.commit()
______

#### setup for lidar sensor

add permission for connecting to serial port `/dev/ttyUSB0` permission denied, `username =  jetboy`. `portname = /dev/ttyUSB0` by: `sudo usermod -a -G dialout <username> & sudo chmod a+rw <portname>`

connect to lidar serial port:

     sudo su
     cd /
     cd dev
     chown <username> ttyUSB0

or:

     cd /dev
     ls t*
     sudo usermod -a -G dialout $USER
______

#### backup and restore os-system

go to `\` as `super user`

     sudo su
     cd /

run command to create backup.tar.gz file

     sudo tar czf /backup.tar.gz\
      --exclude=/backup.tar.gz\
      --exclude=/bin\
      --exclude=/boot\
      --exclude=/dev\
      --exclude=/dist-packages\
      --exclude=/lib\
      --exclude=/lost+found\
      --exclude=/media\
      --exclude=/mnt\
      --exclude=/opt\
      --exclude=/proc\
      --exclude=/root\
      --exclude=/run\
      --exclude=/sbin\
      --exclude=/snap\
      --exclude=/srv\
      --exclude=/sys\
      --exclude=/tmp\
      --exclude=/usr\
      --exclude=/var\
      /

make sure you are root and that you and the backup file are in the root of the filesystem `tar xvpfz backup.tar.gz -C /`
______

#### access robot remotely

- you can use ssh software like PuTTY or if using linux, this os-system is already support ssh into another linux-machine: `ssh [machine_name]@[machine_lan_ip]`, example: `ssh jetboy@192.168.1.9`
______

#### give permission for serial port

if you want to gibve permission for serial port `/dev/ttyUSB0`: `sudo chmod a+rw /dev/ttyUSB0`