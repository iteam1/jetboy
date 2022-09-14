### initialize-guide

**step1**: install a code-editor `bash sublime-text.sh`.

**step2**: install `python3-pip` package: `sudo apt-get update & sudo apt-get install python3-pip`.

**step3**: install python packages virtual enviroment `pip3 install virtualenv`.

**step4**: install pyrealsense for using D455 depth camera `bash pyrealsense.sh`. pyrealsense can not install normally by `pip3`.

**step5**: install opencv `sudo apt-get install python3-opencv` (stable version)

**step6**: install face-recognition `bash face_recognition.sh`.[issuses](http://www.open3d.org/docs/release/arm.html)

**step7**: install jetson-inference by this command `bash jetson-inference.sh`, **run it outsize this repo**.

**step8** : install open3d. [help](https://github.com/isl-org/Open3D/issues/2606#issuecomment-742760659) or Open3D provides experimental support for 64-bit ARM architecture (arm64 or aarch64) on Linux and macOS (Apple Silicon). refer to [ARM support](http://www.open3d.org/docs/release/arm.html).But first try this command:
     
     python3 -m pip install --upgrade pip
     sudo pip3 install open3d==0.13.0

**step9**: install the other required packages by in [requirements.txt](/init/requirements.txt) `pip3 install -r requirements.txt`.

these packages can be install normally by `pip3 install [package_name]`, [requirements.txt](/init/requirements.txt) contain the main packages and their dependencies, bellow is main packages you can install them manually by `pip3 install [package_name]`.

     flask
     flask_sqlalchemy
     sqlite3
     numpy
     pyserial

- export packages into requirements.txt: `pip3 freeze > requirements.txt`.

*Notes:* All packages,libraries and dependencies must be install in gobal. `RPi.GPIO` is build-in package and only can be install on embedded-hardwares like jetson-board or raspberry-board.

**bash-scripts table**

|No|Script|Description|Comment|
|---|---|---|---|
|01|[sublime-text.sh](/init/sublime-text.sh)|install code editor sublime-text|*required*|
|02|[pyrealsense.sh](/init/pyrealsense.sh)|install pyrealsense python library|*required*|
|03|[face_recognition.sh](/init/face_recognition.sh)|install pyrealsense python library|*required*|
|04|[opencv-contrib.sh](/init/opencv-contrib.sh)|install opencv-contrib version for jetson-nano, build from source||
|05|[tensorflow.sh](/init/tensorflow.sh)|install tensorflow for jetson-nano||
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

### check JetPack version

if you want to check your JetPack verison `sudo apt-cache show nvidia-jetpack`
for the version specifically `sudo apt-cache show nvidia-jetpack | grep "Version"`