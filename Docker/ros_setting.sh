#!/bin/bash

## alias
cdls()
{
    \cd "$@" && ls
}
alias cd="cdls"
alias cd_src="cd /root/gym-gazebo/examples/turtlebot"

## environmental variables
export GAZEBO_MODEL_DATABASE_URI=http://models.gazebosim.org/
export ROBOT_INITIAL_POSE="-x 2.7 -y 9.7 -z 0.25 -R 0 -P 0 -Y 0.0"