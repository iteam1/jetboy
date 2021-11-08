from pyrealsense2 import pyrealsense2 as rs
import numpy as np 

class DepthCamera():
	def __init__(self):

		# Configure depth and color streams
		self.pipeline = rs.pipeline()
		config = rs.config()
		pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
		pipeline_profile = config.resolve(pipeline_wrapper)
		self.device = pipeline_profile.get_device()
		device_product_line = str(self.device.get_info(rs.camera_info.product_line))

		config.enable_stream(rs.stream.depth,640,480,rs.format.z16, 30)
		config.enable_stream(rs.stream.color,640,480,rs.format.bgr8,30)

		# Start streaming
		self.pipeline.start(config)

	def get_frame(self):

		# Get frames
		frames = self.pipeline.wait_for_frames()
		depth_frame = frames.get_depth_frame()
		color_frame = frames.get_color_frame()

		# Turn to numpy 
		depth_image = np.asanyarray(depth_frame.get_data())
		color_image = np.asanyarray(color_frame.get_data())


		if not depth_camera or not color_frame:
			return False,None,None

		return True,depth_image,color_image

	def release(self):
		self.pipeline.stop()