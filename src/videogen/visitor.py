#!/usr/bin/env python

class Visitor(object):
    def __init__(self):
        pass
    
    def visit_program_node(self, node):
        pass
    
    def visit_input_file_node(self, node):
        pass
    
    def visit_output_file_node(self, node):
        pass
        
    def visit_configuration_node(self, node):
        pass
            
    def visit_range_node(self, node):
        pass

    def visit_image_node(self, node):
        pass

    def visit_silence_node(self, node):
        pass
    
    def visit_repeat_node(self, node):
        pass
    
class Node(object):
    def __init__(self):
        self._children = []
    
    def accept(self, v):
        pass
    
    def add_child(self, child):
        self._children.append(child)
        
        
        
        
        
        
        
        
        
        
