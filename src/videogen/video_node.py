#!/usr/bin/env python

from visitor import *

class VideoNode(Node):
    def __init__(self):
        pass

    def accept(self, v):
        v.visit_video_node(self)

