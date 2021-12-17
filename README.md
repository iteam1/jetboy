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
    - Do a sp

## Required libraries
    The library with have * mark meaning you can not install it with command `pip install -r requirements.txt`
    *- jetson.GPIO (This libary is built-in jetson-nano board or rasberry pi board, and just can run on this hardware)
    - flask
    - flask_sqlachemy
    - sqlite3
    - tkinter
    *- pyrealsense2 
    - opencv-contrib-python
    - os
    
