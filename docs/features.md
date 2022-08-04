## robot's features & change logs

new features and change logs will be write down in this document

### 31-July-22

**1/ Power supply and electrical system**

- Main power supply is 6Ah-12VDC litium battery (chargeable)
- Voltage and Current metter

*Note:* the current consumption can be increase when boot up, `over current throtted` warning will display on screen or blink yellow power led on main board, that's beacause depth camera d455 consump alot current of main-board jetson nano. The total current can between 0-10 Ampere if only running main-board and 20-30 Ampere when robot's motor run.

**2/ Visual intelligence**

- Depth camera D455 (Intel Realsense)

      Components	
      - Intel RealSense D4
      - Module Intel RealSense D450
      - Bosch BMI055 IMU
      
      Viewspace	86° × 57° (+/- 3°)
      
      Resolution	
      - 1280 × 720 @ 30fps
      - 848 × 480 @ 90fps
      
      Frame per second:	Up to 90 fps
      
      Minimum Depth Distance (Min-Z)	40 cm
      
      Sensor Shutter Type	Global Shutter
      
      Recommended Range	From 0.4 to 6 m
      
      Dimensions	124 mm × 26 mm × 29 mm
      
      Connection Type	USB-C* 3.1 Gen 1

**3/ Manual control**

A local web-server by python web framework Flask

**4/ GPIO control**

### 31-August-22

**1/ Power supply and electrical system**

**2/ Hardware**

**3/ Create 3d map**

**4/ Visual intelligence**
