# DRL-MachineIntelligence
Deep Reinforcement Learning (DRL) project for the Machine Intelligence course

# Gym Documentation
https://www.gymlibrary.ml/

# Gazebo Gym Paper
https://arxiv.org/pdf/1608.05742.pdf%C3%AF%C2%BC%E2%80%B0

# Installation
install docker  

```shell
cd Docker

chmod +x buld.sh

./build.sh
```

# Usage

```shell
cd Docker

chmod +x run.sh

./run.sh
```

In the docker container, type the following. In the first time, the build takes long time, but once you built it, the execution files are retained and the build time will be shortened from the next time.

```shell
bash setup_melodic.bash
```


Refer to: https://github.com/erlerobot/gym-gazebo#usage (Build and install gym-gazebo is already done)

# Tutorial

(After building the ROS package by `bash setup_melodic.bash`)

```shell
cd /root/gym-gazebo/gym_gazebo/envs/installation

bash turtlebot_setup.bash

cd ../../../examples/turtlebot

python circuit2_turtlebot_lidar_qlearn.py
```

# Docker guide

docker ps

open new terminal window with: docker exec -it %container id% bash

# Connecting Gazebo
in a new terminal

```
export GAZEBO_MASTER_URI=http://localhost:XXXXXX #use tbe URI from the initialization

gzclient
```
  
# To do
  
  understanding the code: 
  
  gym_gazebo/envs/turlebot/gazebo.circuit2c_turtlebot_lidar.py
  
  examples/turtlebot/circuit2_turtlebot_lidar_qlearn.py 
  
# Path to worlds
  
  gym-gazebo/gym_gazebo/envs/assets/worlds
