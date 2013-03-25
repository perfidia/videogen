#!/usr/bin/env python

from input_file_node import InputFileNode
from constants import *

class ColorNode(InputFileNode):
    def __init__(self, color):
        self.color = color
        self.type = TYPE_VIDEO
        self._children = []

    def accept(self, v):
        for child in self._children:
            child.accept(v)
            
        v.visit_color_node(self)
        
