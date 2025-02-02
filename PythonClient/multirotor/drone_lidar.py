# Python client example to get Lidar data from a drone
#

import setup_path 
import airsim

import sys
import math
import time
import argparse
import pprint
import numpy

# Makes the drone fly and get Lidar data
class LidarTest:

    def __init__(self):

        # connect to the AirSim simulator
        self.client = airsim.MultirotorClient(ip="192.168.86.61")
        self.client.confirmConnection()
        self.client.enableApiControl(True)

    def execute(self):

        print("arming the drone...")
        self.client.armDisarm(True)

        state = self.client.getMultirotorState()
        s = pprint.pformat(state)
        #print("state: %s" % s)

        airsim.wait_key('Press any key to takeoff')
        #self.client.takeoffAsync().join()

        state = self.client.getMultirotorState()
        #print("state: %s" % pprint.pformat(state))

        airsim.wait_key('Press any key to move vehicle to (-10, 10, -10) at 5 m/s')
        #self.client.moveToPositionAsync(-0, 0, -10, 5).join()

        #self.client.hoverAsync().join()

        airsim.wait_key('Press any key to get Lidar readings')
        
        for i in range(1,2):
            lidarData = self.client.getLidarData();
            if (len(lidarData.point_cloud) < 3):
                print("\tNo points received from Lidar data")
            else:
                points = self.parse_lidarData(lidarData)
                print("\tReading %d: time_stamp: %d number_of_points: %d" % (i, lidarData.time_stamp, len(points)))
                print("\t\tlidar position: %s" % (pprint.pformat(lidarData.pose.position)))
                print("\t\tlidar orientation: %s" % (pprint.pformat(lidarData.pose.orientation)))
                print(' total num of points ', points.shape)
                self.write_lidarData_to_disk(points, i)
                print(points)
            time.sleep(0.1)

    def parse_lidarData(self, data):

        # reshape array of floats to array of [X,Y,Z]
        points = numpy.array(data.point_cloud, dtype=numpy.dtype('f4'))
        points = numpy.reshape(points, (int(points.shape[0]/3), 3))
       
        return points

    def write_lidarData_to_disk(self, points, fid):
        # TODO
        fn="lidardata_"+str(fid)+".ply"
        write_ply(points,fn)
        for i in range(16):
            fn="lidardata_"+str(fid)+"_"+str(i)+".ply"
            write_ply(points[i*64:(i+1)*64],fn)
        print("not yet implemented")

    def stop(self):

        airsim.wait_key('Press any key to reset to original state')

        #self.client.armDisarm(False)
        #self.client.reset()

        self.client.enableApiControl(False)
        print("Done!\n")

def write_ply(points,fn):
    file = open(fn, 'w+', newline ='')
    with file:
        header[3]='element vertex '+str(points.shape[0])
        for i in range(len(header)):
          print(header[i])
          file.write(header[i]+'\n')
        for i in range(len(points)):
          point_str = [str(int) for int in points[i]]
          point_str = " ". join(point_str)
          file.write(point_str+'\n')

header=['ply',
'format ascii 1.0',
'comment VCGLIB generated',
'element vertex 400',
'property float x',
'property float y',
'property float z',
'end_header']
# main
if __name__ == "__main__":
    args = sys.argv
    args.pop(0)

    arg_parser = argparse.ArgumentParser("Lidar.py makes drone fly and gets Lidar data")

    arg_parser.add_argument('-save-to-disk', type=bool, help="save Lidar data to disk", default=False)
  
    args = arg_parser.parse_args(args)    
    lidarTest = LidarTest()
    try:
        lidarTest.execute()
    finally:
        lidarTest.stop()
