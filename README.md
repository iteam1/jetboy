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

## install linux on ubutu 18.0.4

https://linuxize.com/post/how-to-install-pip-on-ubuntu-18.04/

## How to install pyrealsense2 on jetson-nano

https://www.youtube.com/watch?v=EeT-pzM8n-o

https://github.com/IntelRealSense/librealsense

## install realsense-viewer

https://github.com/IntelRealSense/librealsense/blob/master/doc/installation_jetson.md

## install pyrealsesne2 from source [Jetson Error]

https://github.com/IntelRealSense/librealsense/tree/master/wrappers/python

### cmake error

https://stackoverflow.com/questions/16248775/cmake-not-able-to-find-openssl-library

     sudo apt-get install libssl-dev
     
     git clone https://github.com/IntelRealSense/librealsense.git
     
     cd librealsense
     
     mkdir build
     
     cd build
     
     sudo apt-get update && sudo apt-get upgrade
     
Create cmake
     
     cmake ../ -DBUILD_PYTHON_BINDINGS:bool=true -DPYTHON_EXECUTABLE=/usr/bin/python3.6/dist-packages
     
     make -j4
     
     sudo make install

Once you make and install be sure to update your PYTHONPATH:

     
     export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python3.6/dist-packages
    
## install opencv

https://pysource.com/2019/08/26/install-opencv-4-1-on-nvidia-jetson-nano/

https://qengineering.eu/install-opencv-4.5-on-jetson-nano.html


