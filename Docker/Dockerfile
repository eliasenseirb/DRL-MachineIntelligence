# This is an auto generated Dockerfile for ros:robot
# generated from docker_images/create_ros_image.Dockerfile.em
FROM ubuntu:18.04

ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

#######################################################################
##                            install ros                            ##
#######################################################################
RUN apt-get update 
RUN apt-get install -q -y \
    dirmngr \
    gnupg2 \
    lsb-release \
    curl

# setup sources.list
RUN echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list
# setup keys
RUN curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | apt-key add -
RUN apt-get update 
RUN apt install -y \
 ros-melodic-desktop-full 
 # install ros packages
ENV ROS_DISTRO melodic
COPY ./ros_entrypoint.sh /

#install common dependencies
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
   pkg-config \
   apt-utils \
   wget \
   git \
   build-essential \ 
   net-tools \
   gedit \
   terminator \
   nautilus \
   software-properties-common \
   apt-transport-https \
   libopencv-dev \
   ffmpeg \
   x264 \
   libx264-dev \
   zip \
   unzip \
   usbutils \
   sudo \
   python-pip \
   libusb-1.0-0-dev

#######################################################################
##                       install nvidia docker                       ##
#######################################################################
RUN apt-get install -y --no-install-recommends \
    libxau-dev \
    libxdmcp-dev \
    libxcb1-dev \
    libxext-dev \
    libx11-dev \
    mesa-utils \
    x11-apps

# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES ${NVIDIA_VISIBLE_DEVICES:-all}
ENV NVIDIA_DRIVER_CAPABILITIES ${NVIDIA_DRIVER_CAPABILITIES:+$NVIDIA_DRIVER_CAPABILITIES,}graphics

RUN echo "/usr/local/nvidia/lib" >> /etc/ld.so.conf.d/nvidia.conf && \
    echo "/usr/local/nvidia/lib64" >> /etc/ld.so.conf.d/nvidia.conf

# Required for non-glvnd setups.
ENV LD_LIBRARY_PATH /usr/lib/x86_64-linux-gnu:/usr/lib/i386-linux-gnu${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}:/usr/local/nvidia/lib:/usr/local/nvidia/lib64


RUN apt-get install -y python-rosdep
RUN apt-get install -y python-rosinstall
RUN apt-get install -y python-rosinstall-generator
RUN apt-get install -y python-wstool
RUN apt-get install -y build-essential
RUN apt-get install -y 

     
# setup environment
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

ENV ROS_DISTRO melodic

#######################################################################
##                            install Python                            ##
#######################################################################
RUN apt-get update
RUN apt-get install -y python-pip
RUN pip install --upgrade pip


#######################################################################
##                            install Gym                            ##
#######################################################################
WORKDIR /root
RUN apt-get install -y \
    python-pip python3-vcstool python3-pyqt4 \
    pyqt5-dev-tools \
    libbluetooth-dev libspnav-dev \
    pyqt4-dev-tools libcwiid-dev \
    cmake gcc g++ qt4-qmake libqt4-dev \
    libusb-dev libftdi-dev \
    python3-defusedxml python3-vcstool \
    ros-melodic-octomap-msgs        \
    ros-melodic-joy                 \
    ros-melodic-geodesy             \
    ros-melodic-octomap-ros         \
    ros-melodic-control-toolbox     \
    ros-melodic-pluginlib	       \
    ros-melodic-trajectory-msgs     \
    ros-melodic-control-msgs	       \
    ros-melodic-std-srvs 	       \
    ros-melodic-nodelet	       \
    ros-melodic-urdf		       \
    ros-melodic-rviz		       \
    ros-melodic-kdl-conversions     \
    ros-melodic-eigen-conversions   \
    ros-melodic-tf2-sensor-msgs     \
    ros-melodic-pcl-ros \
    ros-melodic-navigation \
    ros-melodic-sophus


RUN pip install gym 
RUN apt-get install python-skimage -y
RUN pip install h5py 
RUN pip install tensorflow-gpu==1.12
RUN pip install numpy==1.15.0
RUN pip install keras 

RUN git clone https://github.com/erlerobot/gym-gazebo.git
WORKDIR /root/gym-gazebo
RUN pip install -e .

WORKDIR /root/gym-gazebo/gym_gazebo/envs/installation