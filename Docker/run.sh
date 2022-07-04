#!/bin/bash

xhost +local:user
nvidia-docker &> /dev/null
if [ $? -ne 0 ]; then
    echo $TAG
    echo "=============================" 
    echo "=nvidia docker not installed="
    echo "============================="
else
    echo "=========================" 
    echo "=nvidia docker installed="
    echo "========================="
    docker run -it \
    --privileged \
    --gpus all \
    --name drl_ml \
    --rm \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v "/$(pwd)/ros_setting.sh:/ros_setting.sh" \
    -v "/$(pwd)/../gym-gazebo:/root/gym-gazebo" \
    -v "/$(pwd)/../models:/root/.gazebo/models" \
    -e DISPLAY=$DISPLAY \
    -v $HOME/.Xauthority:/home/$(id -un)/.Xauthority \
    -e XAUTHORITY=/home/$(id -un)/.Xauthority \
    --net host \
    -e ROS_IP=127.0.0.1 \
    drl-ml:latest
fi