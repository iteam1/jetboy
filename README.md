# Refer links

## NVIDIA

https://www.youtube.com/watch?v=FyrXnNpPR6s&list=PLGs0VKk2DiYxP-ElZ7-QXIERFFPkOuP4_&index=5

https://github.com/NVIDIA

https://www.nvidia.com/en-us/training/online/

https://developer.nvidia.com/embedded/learn/jetson-ai-certification-programs

https://developer.nvidia.com/embedded/twodaystoademo#hello_ai_world

### Jetbot

https://jetbot.org/master/index.html

https://github.com/NVIDIA-AI-IOT/jetbot

## GPIO

![JetsonNano-expansion-pinout](https://user-images.githubusercontent.com/73679364/136185152-faec5c9b-4d30-427f-9b10-27345fca6dde.png)

https://github.com/NVIDIA/jetson-gpio

https://maker.pro/nvidia-jetson/tutorial/how-to-use-gpio-pins-on-jetson-nano-developer-kit

https://circuitpython.readthedocs.io/projects/servokit/en/latest/

     pip3 install adafruit-circuitpython-servokit
sudo pip3 install adafruit-circuitpython-servokit

## Jupyter Notebook

https://youtu.be/g5yWrpwK3C4

https://youtu.be/oaL9N411W-s

## Jetson Nano

![JetsonNano-overview-annotated](https://user-images.githubusercontent.com/73679364/136184979-5444495a-425e-4060-93c1-4807d7fb5831.png)

### AI on the Jetson Nano LESSON 2: Learning the Linux Terminal and Command Line
https://www.youtube.com/watch?v=MfpvdC-QrgY&list=PLGs0VKk2DiYxP-ElZ7-QXIERFFPkOuP4_&index=3

### AI on the Jetson Nano LESSON 3: More Linux Commands
https://www.youtube.com/watch?v=ScgJI9yzMQg&list=PLGs0VKk2DiYxP-ElZ7-QXIERFFPkOuP4_&index=5

### AI on the Jetson Nano LESSON 4: Operating the Jeston Nano Headless
https://www.youtube.com/watch?v=FyrXnNpPR6s&list=PLGs0VKk2DiYxP-ElZ7-QXIERFFPkOuP4_&index=7

### AI on the Jetson Nano LESSON 5: Introduction to Python
https://www.youtube.com/watch?v=_MEEjko2lhA&list=PLGs0VKk2DiYxP-ElZ7-QXIERFFPkOuP4_&index=6

### AI on the Jetson Nano LESSON 31: Controlling Servos with the Jetson Nano using the PCA9685
https://www.youtube.com/watch?v=8YKAtpPSEOk&list=PLGs0VKk2DiYxP-ElZ7-QXIERFFPkOuP4_&index=31

### AI on the Jetson Nano LESSON 32: Tracking an object with Servos in OpenCV
https://www.youtube.com/watch?v=CW7NGWEK1IU&list=PLGs0VKk2DiYxP-ElZ7-QXIERFFPkOuP4_&index=34

### AI on the Jetson Nano LESSON 56: Using the GPIO Pins on the Jetson Nano
https://www.youtube.com/watch?v=BBKpEgJKF0s&list=PLGs0VKk2DiYxP-ElZ7-QXIERFFPkOuP4_&index=56

### AI on the Jetson Nano LESSON 57: Push Button Switch on the GPIO Pins With Pull Up Resistors
https://www.youtube.com/watch?v=ehzrPl5cNCc&list=PLGs0VKk2DiYxP-ElZ7-QXIERFFPkOuP4_&index=58

### AI on the Jetson Nano LESSON 59: PWM on the GPIO Pins of the Jetson Nano
https://www.youtube.com/watch?v=eImDQ0PVu2Y&list=PLGs0VKk2DiYxP-ElZ7-QXIERFFPkOuP4_&index=60

### Jetson Xavier NX: Điều khiển GPIO dạng out
https://www.youtube.com/watch?v=PoJvKbtkcSo

### Nvidia Jetson nano & Node-Red & GPIO pins
https://www.youtube.com/watch?v=30Fj1mo0Uqw

     sudo usermod -aG i2c jetboy 
     sudo groupadd -f -r gpio
     sudo usermod -a -G gpio jetboy
     sudo cp /opt/nvidia/jetson-gpio/etc/99-gpio.rules /etc/udev/rules.d/
     sudo udevadm control –reload-rules && sudo udevadm trigger
     reboot now
     i2cdetect -y -r 1
     
## pwm

     sudo /opt/nvidia/jetson-io/jetson-io.py

# Jetson-Nano

## install opencv

https://pysource.com/2019/08/26/install-opencv-4-1-on-nvidia-jetson-nano/

https://qengineering.eu/install-opencv-4.5-on-jetson-nano.html

https://linuxize.com/post/how-to-install-opencv-on-ubuntu-18-04/ 

## jetpack Tensorflow Realsense

https://www.youtube.com/watch?v=7bUinDUgp5o&t=63s

https://docs.nvidia.com/deeplearning/frameworks/install-tf-jetson-platform/index.html

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
     
## Backup Jetson Nano's Linux system

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
      
## Restore linux with backup.tar 

Make sure you are root and that you and the backup file are in the root of the filesystem.

     tar xvpfz backup.tgz -C /
      
## Stream realsense

https://support.intelrealsense.com/hc/en-us/community/posts/1500000429802-how-to-feed-video-in-web-page-using-flask-app-pyrealsense2-with-opencv-python

https://dev.intelrealsense.com/docs/rs-capture

https://github.com/NakulLakhotia/Live-Streaming-using-OpenCV-Flask

https://titanwolf.org/Network/Articles/Article?AID=6d47b992-6d96-4e42-9393-bd7b50c3836c

## Linux basic command

https://www.puttygen.com/putty-commands

## Connect to rplidar

     sudo su
     cd /
     cd dev
     chown <username> ttyUSB0

or

     cd /dev
     ls t*
     sudo usermod -a -G dialout $USER
