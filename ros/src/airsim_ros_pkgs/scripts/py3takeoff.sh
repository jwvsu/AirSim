#!/bin/bash
source /home/student/bin/py36torch.sh
cd /home/student/Documents/AirSim/ros/src/airsim_ros_pkgs/scripts
rosrun airsim_ros_pkgs takeoff.py --ip asus1
