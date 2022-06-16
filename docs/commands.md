## Commands

This document contain common commands for the repository

### Run all program via bash script

`bash start.sh`

### Run custom program

- Run gpio controller `python3 robot_gpio.py`

- Run gui controller `python3 robot_gui.py`

- Run webserver `python3 robot_server.py`

### Generate database

`python3 gendata.py`

Open terminal:

     ```
     from robot import db
     from robot.models import Robot
     robot = Robot()
     db.session.add(robot)
     db.session.commit()
     ```

### Memos
`/dev/ttyUSB0` permission denied, `username =  jetboy`. `portname = /dev/ttyUSB0`

```
sudo usermod -a -G dialout <username>
sudo chmod a+rw <portname>
```

### Run python from bash

This by default will already run one after the other.

To check that python a.py completed successfully as a required condition for running python b.py, you can do:

     #!/usr/bin/env bash
     python a.py && python b.py

Conversely, attempt to run python a.py, and ONLY run 'python b.py' if python a.py did not terminate successfully:

     #!/usr/bin/env bash
     python a.py || python b.py
     
To run them at the same time as background processes:

     #!/usr/bin/env bash
     python a.py &
     python b.py &

(Responding to comment) - You can chain this for several commands in a row, for example:

python a.py && python b.py && python c.py && python d.py 

### Install sublime-text

     sudo apt update

     sudo apt install dirmngr gnupg apt-transport-https ca-certificates software-properties-common

     curl -fsSL https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -

     sudo add-apt-repository "deb https://download.sublimetext.com/ apt/stable/"

     sudo apt install sublime-text

### GPIO

     pip3 install adafruit-circuitpython-servokit
     
     sudo pip3 install adafruit-circuitpython-servokit

### Nvidia Jetson nano & Node-Red & GPIO pins
https://www.youtube.com/watch?v=30Fj1mo0Uqw

     sudo usermod -aG i2c jetboy 
     sudo groupadd -f -r gpio
     sudo usermod -a -G gpio jetboy
     sudo cp /opt/nvidia/jetson-gpio/etc/99-gpio.rules /etc/udev/rules.d/
     sudo udevadm control –reload-rules && sudo udevadm trigger
     reboot now
     i2cdetect -y -r 1
     
### pwm

     sudo /opt/nvidia/jetson-io/jetson-io.py

### jetpack Tensorflow Realsense

     sudo apt-get update
     
     sudo apt-get install libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev liblapack-dev libblas-dev gfortran
     
     sudo apt-get install python3-pip
     
     sudo pip3 install -U pip testresources setuptools==49.6.0
     
     sudo pip3 install -U --no-deps numpy==1.19.4 future==0.18.2 mock==3.0.5 keras_preprocessing==1.1.2 keras_applications==1.0.8 gast==0.4.0 protobuf pybind11 cython pkgconfig
     
     sudo env H5PY_SETUP_REQUIRES=0 pip3 install -U h5py==3.1.0
     
     sudo pip3 install --pre --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v46 'tensorflow<2'

Check what jetpack we are using 

     cat/etc/nv_tegra_release

Check the GPU begin recognize corectlly

     import tensorflow as tf
     
     print(tf.__version__)
     print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))

Install Pyrealsense on jetson nano

     git clone https://github.com/JetsonHacksNano/installLibrealsense.git
     
Correct the cuda version in buildLibrealsense.sh file
     
     NVCC_PATH=/usr/local/cuda-10.2/bin/nvcc
     
Execute buildLibrealsense file
     
     ./buildLibrealsense.sh
     
Refesh your current shell invironment
     
     source ~/.bashrc
     
Install some libraries

     sudo pip3 install -U pip keras==2.1.5
     
     sudo pip3 install -U pip pillow
     
     sudo pip3 install matplotlib
     
     sudo apt-get install libcanberra-gtk*

Open the karas-yolo page: https://github.com/qqwweee/keras-yolo3

     git clone https://github.com/qqwweee/keras-yolo3.git
     
     cd keras-yolo3
     
Download the weight

     wget https://pjreddie.com/media/files/yolov3-tiny.weights
     
Convert to h5 files

     python3 convert.py yolov3-tiny.cfg yolov3-tiny.weights model_data/yolo-tiny.h5
     
Modify the tiny-yolo.py

     "model_path": 'model_data/yolo-tiny.h5',
     "anchors_path": 'model_data/tiny_yolo_anchors.txt',

Run

     python3 yolo.py
     
### Backup Jetson Nano's Linux system

Go to \

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
      
### Restore linux with backup.tar 

Make sure you are root and that you and the backup file are in the root of the filesystem.

     tar xvpfz backup.tar.gz -C /
      

### Connect to rplidar

     sudo su
     cd /
     cd dev
     chown <username> ttyUSB0

or

     cd /dev
     ls t*
     sudo usermod -a -G dialout $USER
     