#!/usr/bin/env python

from input_file_node import InputFileNode

class ImageNode(InputFileNode):
    def __init__(self, path):
        super(ImageNode, self).__init__(path)

    def accept(self, v):
        v.visit_image_node(self)
        
