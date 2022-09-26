'''
Author: locchuong
Updated: 26/9/22
Description:
    Test stream camera via jetson_utils in many source
    MIPI CSI cameras:
    	video-viewer csi://0
    	video-viewer csi://0 output.mp4
    	video-viewer csi://0 rtp://<remote-ip>:1234
    (*)V4L2 cameras:
    	video-viewer v4l2:///dev/video0
    	video-viewer /dev/video
    	video-viewer /dev/video0 output.mp4
    	video-viewer /dev/video0 rtp://<remote-ip>:123
    RTP:
    	video-viewer --input-codec=h264 rtp://@:1234
    	video-viewer --input-codec=h264 rtp://224.0.0.0:1234
    Transmitting RTP:
    	video-viewer --bitrate=1000000 csi://0 rtp://<remote-ip>:1234
    	video-viewer --output-codec=h265 my_video.mp4 rtp://<remote-ip>:1234
    RTSP:
    	video-viewer rtsp://<remote-ip>:1234 my_video.mp4
    	video-viewer rtsp://username:password@<remote-ip>:1234
    
'''
import jetson.utils # jetson_utils
import argparse
import sys

# parse command line
parser = argparse.ArgumentParser()
parser.add_argument("input_URI",type=str,help="URI of the input stream")
parser.add_argument("output_URI",type=str,default="",nargs="?",help="URI of the output stream")
opt = parser.parse_known_args()[0]

# create video sourcs outputs
input = jetson.utils.videoSource(opt.input_URI,argv=sys.argv)
output = jetson.utils.videoOutput(opt.output_URI,argv=sys.argv)

if __name__  == "__main__":
	while output.IsStreaming():
		image = input.Capture(format='rgb8') # can also be format 'rgba8','rgb32f','rgba32f'
		output.Render(image)
		output.SetStatus("Video Viewer | {:d}x{:d} | {:.1f} FPS".format(image.width,image.height,output.GetFrameRate()))

