#!/usr/bin/env python

from visitor import *

class ConfigurationNode(Node):
    def __init__(self, x, y, fps, sar=-1, video_codec = "libx264", audio_codec = "libmp3lame"):
        self.x = x
        self.y = y
        self.fps = fps
        self.sar = sar
        self.video_codec = video_codec
        self.audio_codec = audio_codec
        
        if sar == -1 and (x != None or y != None):
            self.sar = float(x)/float(y)
            

    def accept(self, v):
        v.visit_configuration_node(self)
        
