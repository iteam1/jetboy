### repo utils

|No|Program|Description|Comment|
|---|---|---|---|
|01|[test_arm.py](/utils/test_arm.py)|test serial-communication by protocol with robot's arm module||
|02|[test_serial.py](/utils/test_serial.py)|test serial-communication with microcontroller arduino-nano, connect to serial port ex: `COM4` on Windows or `dev/ttyUSB0` on linux and send a string `90,90,90,90,90,1a`, microcontroller will read serial until `a` character and compare the previous part, if equal `90,90,90,90,90` then blink led|refer to embeded code [test_uart](https://github.com/iteam1/robot-jetboy/tree/main/embed/test_uart),[uart2uart](https://github.com/iteam1/robot-jetboy/tree/main/embed/uart2uart)|
|03|[read_db.py](/utils/read_db.py)|test serial-communication with arudino chip|`python3 -n 1 /utils/read_db.py`|
|04|[stream_d455.py](/utils/stream_d455.py)|test stream depth camera d455 by pyrealsense and opencv|depend on module [realsense_depth.py](/utils/realsense_depth.py)|
|05|[stream_cam.py](/utils/stream_cam.py)|test stream serial camera by opencv|can not run, robot's hardware only got depth-camera|
|06|[test_sensor.py](/utils/test_sensor.py)|test ultra-sonic sensors signal||
|07|[rplidar.py](/utils/rplidar.py)|get info from serial RPlidar A1||
|08|[track_marker.py](/utils/track_marker.py)|control robot follow a target aruco-marker's id|required opencv-contrib for using aruco module, this package is no longer used in this repo, for reference purposes only|
|09|[view_cloud.py](/utils/view_cloud.py)|view a single point cloud file `.ply` file captured by depth camera||
|10|[pyrealsense2](/utils/pyrealsense2)|this is not a util program, if you want to use pyrealsense package installed by build from source C, you have to add this floder into the directory where you store the util program use pyrealsense, similar [realsense_depth.py](/utils/realsense_depth.py)||
