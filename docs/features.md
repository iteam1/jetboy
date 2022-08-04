## robot's features & change logs

new features and change logs will be write down in this document

### 31-July-22

**1/ Power supply and electrical system**

- Main power supply is 6Ah-12VDC litium battery (chargeable)
- Voltage and Current metter

*Note:* the current consumption can be increase when boot up, `over current throtted` warning will display on screen and yellow power led on main board blink, that's beacause depth camera d455 consump alot current of main-board jetson nano. The total current can between 0-10 Ampere if only running main-board and 20-30 Ampere when robot's motor run.

**2/ Visual intelligence**

- Depth camera D455 (Intel Realsense)

      -Components	
            - Intel RealSense D4
            - Module Intel RealSense D450
            - Bosch BMI055 IMU
      - Viewspace	86° × 57° (+/- 3°)
      - Resolution	
            - 1280 × 720 @ 30fps
            - 848 × 480 @ 90fps
      - Frame per second:	Up to 90 fps
      - Minimum Depth Distance (Min-Z: 40 cm
      - Sensor Shutter Type: Global Shutter
      - Recommended Range: From 0.4 to 6 m
      - Dimensions: 124 mm × 26 mm × 29 mm
      - Connection Type: USB-C* 3.1 Gen 1

**3/ Manual control**

A local web-server by python web framework Flask help user can control robot manually, streaming camera frame,etc. Check [apidocs](/docs/apidocs.md) for more information.

**4/ GPIO control**

Module `gpio.py` contain class for controlling motor, arm,etc. 

### 31-August-22

**1/ Power supply and electrical system**

- Expand power from 6Ah-12VDC into 12Ah-VDC

- Separate main-board power source and the others (actuators, sensors,etc.)
 
**2/ Hardware**

**3/ Create 3d map**

Create a 3D map with [Open3D](http://www.open3d.org/docs/release/getting_started.html#python) and moving-log

**4/ Visual intelligence**

Apply machine learning vision models by [jetson-inference](https://github.com/dusty-nv/jetson-inference)
