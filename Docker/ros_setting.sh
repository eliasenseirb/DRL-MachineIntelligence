#!/bin/bash

## alias
cdls()
{
    \cd "$@" && ls
}
alias cd="cdls"
alias cd_src="cd /root/gym-gazebo/examples/turtlebot"
alias cd_installation="cd /root/gym-gazebo/gym_gazebo/envs/installation"

## environmental variables
export GAZEBO_MODEL_DATABASE_URI=http://models.gazebosim.org/
export ROBOT_INITIAL_POSE="-x 2.7 -y 2.7 -z 0.25 -R 0 -P 0 -Y -1.57"
export GOAL_X="-3.0"
export GOAL_Y="-9.0"