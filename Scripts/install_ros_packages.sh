#!/bin/bash

echo Script para paquetes ros2

echo Instalación de varios paquetes

sleep 1s

cd /home/ros

sudo apt-get update

sudo apt-get upgrade

sudo apt-get install ros-humble-ros2-controllers
sudo apt-get install ros-humble-gazebo-ros
sudo apt-get install ros-humble-gazebo-ros-pkgs
sudo apt-get install ros-humble-ros2-control
sudo apt-get install ros-humble-gazebo-ros2-control
sudo apt-get install ros-humble-joint-state-publisher-gui
sudo apt-get install ros-humble-turtlesim
sudo apt-get install ros-humble-robot-localization
sudo apt-get install ros-humble-joy
sudo apt-get install ros-humble-joy-teleop
sudo apt-get install ros-humble-tf-transformations
sudo apt-get install ros-humble-plotjuggler
sudo apt-get install ros-humble-plotjuggler-ros
