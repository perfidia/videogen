#!/usr/bin/env python

from visitor import *
from input_file_node import *

class ProgramNode(Node):
    def __init__(self, path):
        self._children = []
        self.path = path
        self.overwrite = False
        
    def accept(self, v):
        for child in self._children:
            child.accept(v)
            
        v.visit_program_node(self);