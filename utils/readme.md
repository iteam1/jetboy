### repo utils

|No|Program|Description|Comment|
|---|---|---|---|
|01|[test_arm.py](/utils/test_arm.py)|test serial-communication by protocol with robot's arm module|---|
|02|[test_serial.py](/utils/test_serial.py)|test serial-communication with arudino chip||
|03|[read_db.py](/utils/read_db.py)|test serial-communication with arudino chip|`python3 -n 1/utils/read_db.py`|
|04|[stream_d455.py](/utils/stream_d455.py)|test stream depth camera d455 by pyrealsense|depend on module [realsense_depth.py](/utils/realsense_depth.py)|
|05|[stream_cam.py](/utils/stream_cam.py)|test stream serial camera d455 by pyrealsense||
|06|[test_sensor.py](/utils/test_sensor.py)|test ultra-sonic sensors signal||
|07|[rplidar.py](/utils/rplidar.py)|get info from serial RPlidar A1||
|08|[track_marker.py](/utils/track_marker.py)|control robot follow a target aruco-marker's id||
|09|[view_cloud.py](/utils/view_cloud.py)|view a single point cloud file `.ply` file captured by depth camera||