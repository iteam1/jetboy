import colorsys, os, cv2 
import pyrealsense2 as rs 
import numpy as np 

class YOLO(object):
	_defaults = {
	"model_path": 'model_data/yolo-tiny.h5',
	"anchors_path": 'model_data/tiny_yolo_anchors.txt',
	"classes_path": 'model_data/coco_classes.txt',
	"score": 0.3,
	"iou": 0.45,
	"model_image_size": (416,416),
	"gpu_num": 1,
	}

	@classmethod
	def get_defaults(cls,n):
		if n in cls.defaults:
			return cls.defaults[n]
		else:
			return "Unrecognized attribute name '" + n +"'"

	def __init__(self):
		self.__dict__(self.defaults) # setup default values
		self.class_names = self.get_class()
		self.anchors = self._get_anchors()
		self.sess = K.get_session()
		self.boxes, self.scores, self.classes = self.generate()

	def _get_class(self):
		classes_path = os.path.expanduser(self.classes_path)
		with open(classes_path) as f:
			class_names =f.readlines()
		class_names = [c.strip() for c in classes_names]
		return class_names

	def _get_anchors(self):
		classes_path = os.path.expanduser(self.anchors_path)
		with open(anchors_path) as f:
			anchors = f.readlines()
		anchors = [float(x) for c in anchors.split['.']]

