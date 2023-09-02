#!/usr/bin/env python
#
# Software License Agreement (BSD)
#
# \file      invert_cam.py
# \authors   Jeremy Fix <jeremy.fix@centralesupelec.fr>
# \copyright Copyright (c) 2022, CentraleSupélec, All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#  * Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation and/or
#    other materials provided with the distribution.
#  * Neither the name of Autonomy Lab nor the names of its contributors may be
#    used to endorse or promote products derived from this software without specific
#    prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WAR- RANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, IN- DIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

# External imports
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image, CompressedImage


class ImageFlipper(Node):
    def __init__(self):
        super().__init__("republish")
        self.bridge = CvBridge()

        self.img_pub = self.create_publisher(CompressedImage, "out", 1)
        self.img_sub = self.create_subscription(CompressedImage, "in", self.on_image, 1)

    def on_image(self, msg):
        frame = self.bridge.compressed_imgmsg_to_cv2(msg, "bgr8")
        # Vertically and horizontally flip the image
        frame = frame[::-1, ::-1, :]
        self.img_pub.publish(self.bridge.cv2_to_compressed_imgmsg(frame))


def main(args=None):
    rclpy.init(args=args)

    flipper_node = ImageFlipper()
    rclpy.spin(flipper_node)

    flipper_node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
