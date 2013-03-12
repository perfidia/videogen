#!/usr/bin/env python

from input_file_node import InputFileNode

class ConcatNode(InputFileNode):
    def __init__(self):
        self._children = []

    def accept(self, v):
        for child in self._children:
            child.accept(v)
            
        v.visit_concat_node(self)

