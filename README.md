# DRL-MachineIntelligence
Deep Reinforcement Learning (DRL) project for the Machine Intelligence course

![simulation_image](https://raw.githubusercontent.com/eliasenseirb/DRL-MachineIntelligence/main/Images/simulation_image.png)

## Assumed Environment
- Ubuntu 20.04

(Maybe other versions are available ecause we use docker)

## Requirements
- docker
- nvidia-docker

[How to install](https://takake-blog.com/ubutnu2004-install-nvidia-docker/)

## Installation

```shell
git clone https://github.com/eliasenseirb/DRL-MachineIntelligence.git
cd Docker
chmod +x build.sh
./build.sh
```

## Usage
### Run docker container and enter its terminal

```shell
cd Docker
chmod +x run.sh
./run.sh
```

### Run simulation

```shell
source setup_melodic.bash
source setup_turtlebot.bash
cd_src
python cafe_turtlebot_lidar_qlearn.py
```

Note: In the first time, `bash setup_melodic.bash` builds the ROS packages and it takes long time. But once you built it, the execution files are retained and the build time will be shortened from the next time.

### Watch the simulation in Gazebo
Create new terminal and enter the exiisting docker container's terminal

```shell
cd Docker
chmod +x new_terminal.sh
./new_terminal.sh
```

Setup the environment and launch Gazebo

```shell
source setup_melodic.bash
source setup_turtlebot.bash
source setup_display.bash
gzclient
```

## Tips

### Change initial robot position
export "ROBOT_INITIAL_POSE" environment variable like this

```shell
export ROBOT_INITIAL_POSE="-x 2.7 -y 2.7 -z 0.25 -R 0 -P 0 -Y -1.57"
```

### Change goal position
export "GOAL_X" and "GOAL_Y" environment variablse like this

```shell
export GOAL_X="-3.0"
export GOAL_Y="-9.0"
```

## Q. How to create own environment?

A. See [this commit](https://github.com/eliasenseirb/DRL-MachineIntelligence/commit/527b512f4c2a17dfa9b10829542bcb381662ad48)

# Reference
## Gym Documentation
https://www.gymlibrary.ml/

## Gazebo Gym Paper
https://arxiv.org/pdf/1608.05742.pdf%C3%AF%C2%BC%E2%80%B0


  

  

