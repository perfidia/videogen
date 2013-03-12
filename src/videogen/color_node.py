#!/usr/bin/env python

from input_file_node import InputFileNode

class ColorNode(InputFileNode):
    def __init__(self, color):
        self.color = color

    def accept(self, v):
        v.visit_color_node(self)
        
