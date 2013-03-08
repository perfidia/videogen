#!/usr/bin/env python

from visitor import *

class RepeatNode(Node):
    def __init__(self, times):
        self.times = times

    def accept(self, v):
        v.visit_repeat_node(self)
        
