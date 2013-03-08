#!/usr/bin/env python

class Visitor(object):
    def __init__(self):
        pass
    
    def visit_node(self):
        pass
    
class Node(object):
    def __init__(self):
        self._children = []
    
    def accept(self, v):
        pass
    
    def add_child(self, child):
        self._children.append(child)