#!/usr/bin/env python

from visitor import *

class SilenceNode(Node):
    def __init__(self):
        pass

    def accept(self, v):
        v.visit_silence_node(self)
        
