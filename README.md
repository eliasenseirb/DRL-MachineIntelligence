# DRL-MachineIntelligence
Deep Reinforcement Learning (DRL) project for the Machine Intelligence course

# Gym Documentation
https://www.gymlibrary.ml/

# Gazebo Gym Paper
https://arxiv.org/pdf/1608.05742.pdf%C3%AF%C2%BC%E2%80%B0

# Installation
install docker  

```
cd Docker

./build.sh
```

# Usage

```shell
cd Docker

./run.sh
```

Refer to: https://github.com/erlerobot/gym-gazebo#usage (Build and install gym-gazebo is already done)

# Tutorial

```
bash turtlebot_setup.bash

cd ../../../examples/turtlebot

python circuit2_turtlebot_lidar_qlearn.py
```

# Docker guide

open new terminal window with docker exec -it <container name> bash
  
# To do
  
  understanding the code: 
  
  gym_gazebo/envs/turlebot/gazebo.circuit2c_turtlebot_lidar.py
  
  examples/turtlebot/circuit2_turtlebot_lidar_qlearn.py 
  
# 1. Question How is the simulation environment loaded in and how can we change it to ours?
