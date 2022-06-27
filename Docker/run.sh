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
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -e DISPLAY=$DISPLAY \
    -v $HOME/.Xauthority:/home/$(id -un)/.Xauthority \
    -e XAUTHORITY=/home/$(id -un)/.Xauthority \
    --net host \
    -e ROS_IP=127.0.0.1 \
    -e GAZEBO_MASTER_URI=http://localhost:13853 \
    drl-ml:latest
fi