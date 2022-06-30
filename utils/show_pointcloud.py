'''
Author: locchuong
Updated: 10/2/22
Description:
    - Show pointcloud .ply file
'''
import open3d as o3d
import numpy as np 
import argparse  

parser = argparse.ArgumentParser(description = "Show pointcloud .ply file")
parser.add_argument('-d','--directory',type = str,help='the directory to pointcloud',required = True)
args = parser.parse_args()

if __name__ == "__main__":

	# show point cloud
	print("Load a ply point cloud cloud, print it and render it")
	pcd = o3d.io.read_point_cloud(args.directory)
	print(pcd)
	print(np.asarray(pcd.points))
	o3d.visualization.draw_geometries([pcd])