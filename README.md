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

chmod +x build.sh

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

# Cafe Environment

```
cd ../../../examples/turtlebot

export GAZEBO_MODEL_DATABASE_URI=http://models.gazebosim.org/

export ROBOT_INITIAL_POSE="-x 2.7 -y 9.7 -z 0.25 -R 0 -P 0 -Y 0.0"


python cafe_turtlebot_lidar_qlearn.py
```

Q. How to create own environment?

A. See [this commit](https://github.com/eliasenseirb/DRL-MachineIntelligence/commit/527b512f4c2a17dfa9b10829542bcb381662ad48)
  

  

