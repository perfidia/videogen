#!/usr/bin/env python

from visitor import *

class OutputFileNode(Node):
    def __init__(self, path):
        self.path = path
        self._children = []

    def accept(self, v):
        for child in self._children:
            child.accept(v)
            
        v.visit_output_file_node(self)
        
