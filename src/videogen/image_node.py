#!/usr/bin/env python

from input_file_node import InputFileNode
from constants import *

class ImageNode(InputFileNode):
    def __init__(self, path):
        super(ImageNode, self).__init__(path, TYPE_VIDEO)

    def accept(self, v):
        for child in self._children:
            child.accept(v)
            
        v.visit_image_node(self)
        
