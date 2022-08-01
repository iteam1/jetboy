### initilize-guide

**step1**: install a code-editor `bash sublime-text.sh` 

**step2**: install `python3-pip` package: `sudo apt-get update & sudo apt-get install python3-pip`

**step3**: install python packages virtual enviroment `pip3 install virtualenv`
______

**init database**

the database `sqlite3` is already there in the repo, but if you lost it, in `/utils` folder Run python script for generate a sqlite database: python3 gendata.py

open terminal:

	from robot import db
	from robot.models import Robot
	robot = Robot()
	db.session.add(robot)
	db.session.commit()
______

**setup for lidar sensor**

add permission for connecting to serial port

	 /dev/ttyUSB0` permission denied, `username =  jetboy`. `portname = /dev/ttyUSB0

by: `sudo usermod -a -G dialout <username> & sudo chmod a+rw <portname>`

connect to lidar serial port:

     sudo su
     cd /
     cd dev
     chown <username> ttyUSB0

or

     cd /dev
     ls t*
     sudo usermod -a -G dialout $USER
______

**backup and restore os-system**

Go to `\` as `super user`

     sudo su
     
     cd /

Run command to create backup.tar.gz file

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
______

**14/ Restore linux with backup.tar**

Make sure you are root and that you and the backup file are in the root of the filesystem.

     tar xvpfz backup.tar.gz -C /
      
______
