#!/usr/bin/env python

from visitor import *

class AudioNode(Node):
    def __init__(self):
        pass

    def accept(self, v):
        v.visit_audio_node(self)

