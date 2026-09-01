#!/usr/bin/env bash

# Install the additional ROS 2 Humble packages used by this project.
set -Eeuo pipefail

ROS_DISTRO="humble"

fail() {
    printf '\nError: %s\n' "$*" >&2
    exit 1
}

if [[ "${EUID}" -eq 0 ]]; then
    fail "Run this script as a regular user. It will request sudo when needed."
fi

if [[ ! -f "/opt/ros/${ROS_DISTRO}/setup.bash" ]]; then
    fail "ROS 2 Humble is not installed. Run ros2_install.sh first."
fi

if [[ -r /etc/os-release ]]; then
    # shellcheck disable=SC1091
    source /etc/os-release
    if [[ "${ID:-}" != "ubuntu" || "${VERSION_CODENAME:-}" != "jammy" ]]; then
        fail "These packages target ROS 2 Humble on Ubuntu 22.04 Jammy."
    fi
fi

sudo apt update
sudo apt install -y \
    "ros-${ROS_DISTRO}-ros2-controllers" \
    "ros-${ROS_DISTRO}-gazebo-ros" \
    "ros-${ROS_DISTRO}-gazebo-ros-pkgs" \
    "ros-${ROS_DISTRO}-ros2-control" \
    "ros-${ROS_DISTRO}-gazebo-ros2-control" \
    "ros-${ROS_DISTRO}-joint-state-publisher-gui" \
    "ros-${ROS_DISTRO}-turtlesim" \
    "ros-${ROS_DISTRO}-robot-localization" \
    "ros-${ROS_DISTRO}-joy" \
    "ros-${ROS_DISTRO}-joy-teleop" \
    "ros-${ROS_DISTRO}-tf-transformations" \
    "ros-${ROS_DISTRO}-plotjuggler" \
    "ros-${ROS_DISTRO}-plotjuggler-ros"

printf '\nAdditional ROS 2 Humble packages installed successfully.\n'
