#!/usr/bin/env python

from visitor import Visitor

from program_node import ProgramNode

class FFMpegVisitor(Visitor):
    def __init__(self):
        self._program = "";
        self._inputs = "";
        self._output = "";
        self._options = "";
        self._stack = []
    
    def get_command(self):
        space = " "
        return self._program + space + self._inputs + space + self._options + space + self._output
    
    def visit_program_node(self, node):
        self._program = node.path
    
    def visit_input_file_node(self, node):
        self._inputs = self._inputs + " -i " + node.path;
    
    def visit_output_file_node(self, node):
        self._output = node.path
        
    def visit_configuration_node(self, node):
        if node.x != None and node.y != None:
            self._options = self._options + " -s " + str(node.x) + "x" + str(node.y)
        if node.fps != None:
            self._options = self._options + " -r " + str(node.fps)
