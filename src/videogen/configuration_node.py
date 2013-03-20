#!/usr/bin/env python

from visitor import *

class ConfigurationNode(Node):
    def __init__(self, x, y, fps, sar=-1):
        self.x = x
        self.y = y
        self.fps = fps
        self.sar = sar
        
        if sar == -1:
            self.sar = float(x)/float(y)
            

    def accept(self, v):
        v.visit_configuration_node(self)
        
