#!/usr/bin/env python

from visitor import *

class InputFileNode(Node):
    def __init__(self, path):
        self.path = path

    def accept(self, v):
        v.visit_input_file_node(self)