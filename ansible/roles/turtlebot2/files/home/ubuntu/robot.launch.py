#!/usr/bin/env python3
#
#
# Authors: Jeremy Fix

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node


def generate_launch_description():
    KOBUKI_LAUNCH_FILE = "/kobuki_node-launch.py"
    kobuki_pkg_dir = LaunchConfiguration(
        "kobuki_pkg_dir",
        default=os.path.join(get_package_share_directory("kobuki_node"), "launch"),
    )

    LDS_LAUNCH_FILE = "/hlds_laser.launch.py"
    lidar_pkg_dir = LaunchConfiguration(
        "lidar_pkg_dir",
        default=os.path.join(
            get_package_share_directory("hls_lfcd_lds_driver"), "launch"
        ),
    )

    OPENNI2_LAUNCH_FILE = "/camera_only.launch.py"
    openni2_pkg_dir = LaunchConfiguration(
        "openni2_pkg_dir",
        default=os.path.join(get_package_share_directory("openni2_camera"), "launch"),
    )

    return LaunchDescription(
        [
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource([kobuki_pkg_dir, KOBUKI_LAUNCH_FILE])
            ),
            Node(
                package='hls_lfcd_lds_driver',
                executable='hlds_laser_publisher',
                name='hlds_laser_publisher',
                parameters=[{'port': "/dev/LDS01", 'frame_id': "base_scan"}],
                remappings=[('/scan', '/scan_raw')]
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource([openni2_pkg_dir, OPENNI2_LAUNCH_FILE]),
                launch_arguments={}.items(),
            ),
            Node(
                package="tf2_ros",
                executable="static_transform_publisher",
                name="lds_to_base",
                arguments="0 0 0.24 0 0 0 1 base_link base_scan".split(),
            ),
            Node(
                package="tf2_ros",
                executable="static_transform_publisher",
                name="base_link_to_base_footprint",
                arguments="0 0 0 0 0 0 1 base_footprint base_link".split(),
            ),
            Node(
                package="laser_filters",
                executable="scan_to_scan_filter_chain",
                parameters=["/home/ubuntu/range_filter.yaml"],
                remappings=[('/scan', '/scan_raw'), ('/scan_filtered', '/scan')]
            ),
        ]
    )
