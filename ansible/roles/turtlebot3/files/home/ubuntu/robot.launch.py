#!/usr/bin/env python3
#
#
# Authors: Jeremy Fix

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    turtlebot3_pkg_dir = LaunchConfiguration(
        "turtlebot3_bringup",
        default=os.path.join(
            get_package_share_directory("turtlebot3_bringup"), "launch/"
        ),
    )

    return LaunchDescription(
        [
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource([turtlebot3_pkg_dir, "robot.launch.py"])
            ),
            # Add the camera node
            Node(
                package="v4l2_camera",
                executable="v4l2_camera_node",
                name="camera",
                remappings=[
                    ("/image_raw", "/base_image_raw"),
                    ("/image_raw/compressed", "/base_image_raw/compressed"),
                ],
            ),
            Node(
                package="st5",
                executable="invert_cam",
                name="camera_inverter",
                remappings=[
                    ("in", "/base_image_raw/compressed"),
                    ("out", "/image_raw/compressed"),
                ],
            ),
        ]
    )
