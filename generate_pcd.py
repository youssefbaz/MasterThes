import argparse
import sys
import os
from PIL import Image
import pptk
import numpy as np
import glob
import cv2

focalLength = 1640.0
centerX = 0
centerY = 0
scalingFactor = 500

def generate_pointcloud():#rgb_file="",depth_file="",ply_file=""):
    print("point cloud")
    rgb_file="C:/Users/Youssef/Desktop/Tour.jpeg"
    depth_file="C:/Users/Youssef/Desktop/Dub3.jpeg"
    ply_file = "C:/Users/Youssef/Desktop/finalll.ply"
    rgb = Image.open(rgb_file)
  
    depth = Image.open(depth_file).convert('I')
    if rgb.size != depth.size:
        raise Exception("Color and depth image do not have the same resolution.")
    if rgb.mode != "RGB":
        raise Exception("Color image is not in RGB format")
    if depth.mode != "I":
        raise Exception("Depth image is not in intensity format")

    points = []
    print(str(rgb.size[0])+" x "+str(rgb.size[1]))
    for v in range(rgb.size[1]):
        for u in range(rgb.size[0]):
            color = rgb.getpixel((u,v))
            Z = depth.getpixel((u,v))
            Z = -5064 * np.log(Z) + 31489
            Z = Z / scalingFactor
            #print(Z)
            #print(u)
            #print(v)
            if Z==0: continue
            X = (u - centerX) * Z / focalLength
            Y = (v - centerY) * Z / focalLength
            points.append("%f %f %f %d %d %d 0\n"%(X,Y,Z,color[0],color[1],color[2]))
        #points.append("%f %f %f %d %d %d 0\n" % (X, Y, Z, color[0], color[1], color[2]))
        #pptk.viewer(points)
    file = open(ply_file, "w")
    file.write('''ply
        format ascii 1.0
        element vertex %d
        property float x
        property float y
        property float z
        property uchar red
        property uchar green
        property uchar blue
        property uchar alpha
        end_header
        %s
        ''' % (len(points), "".join(points)))
    file.close()
    # pptk.viewer(plyf_iole)


if __name__ == '__main__':
    generate_pointcloud()
    if False:
        parser = argparse.ArgumentParser(description='''
                This script reads a registered pair of color and depth images and generates a colored 3D point cloud in the
                PLY format. 
                ''')
        parser.add_argument('rgb_file', help='input color image (format: png)')
        parser.add_argument('depth_file', help='input depth image (format: png)')
        parser.add_argument('ply_file', help='output PLY file (format: ply)')
        args = parser.parse_args()

        generate_pointcloud(args.rgb_file, args.depth_file, args.ply_file)
