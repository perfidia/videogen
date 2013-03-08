#!/usr/bin/env python

from visitor import *

class ConfigurationNode(Node):
    def __init__(self, x, y, fps):
        self.x = x
        self.y = y
        self.fps = fps

    def accept(self, v):
        v.visit_configuration_node(self)
        
