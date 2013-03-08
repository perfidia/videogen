#!/usr/bin/env python

from visitor import *

class RangeNode(Node):
    def __init__(self, start, duration):
        self.start = start
        self.duration = duration

    def accept(self, v):
        v.visit_range_node(self)
        
