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
parser.add_argument('-f','--filename',type = str,help='the name of pointcloud',required = True)
args = parser.parse_args()

if __name__ == "__main__":

	# show point cloud
	print("Load a ply point cloud cloud, print it and render it")
	pcd = o3d.io.read_point_cloud("./pointcloud/" + args.filename + ".ply")
	print(pcd)
	print(np.asarray(pcd.points))
	o3d.visualization.draw_geometries([pcd])