#!/usr/bin/env python

from visitor import *

class InputFileNode(Node):
    def __init__(self, path, type):
        self.path = path
        self.type = type
        self._children = []

    def accept(self, v):
        for child in self._children:
            child.accept(v)
            
        v.visit_input_file_node(self)