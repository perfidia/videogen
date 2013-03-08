#!/usr/bin/env python

from visitor import Visitor

from program_node import ProgramNode

import copy

class FFMpegVisitor(Visitor):
    def __init__(self):
        self._program = "";
        self._inputs = [];
        self._output = "";
        self._options = {};
        
        self._tempInputOptionsMap = {}
    
    def get_command(self):
        space = " "
        inputs = ""
        
        for input in self._inputs:
            inp = input["options"]
            
            for option in inp:
                inputs = inputs + space + option
                if inp[option] != "":
                    inputs = inputs + space + inp[option]
            
            inputs = inputs + space + "-i" + space + input["path"]
            
        options = ""
            
        for option in self._options:
            options = options + space + option
            if self._options[option] != "":
                options = options + space + self._options[option]
                
        command = self._program + inputs
        
        if options == "":
            command = command + space
            
        command = command + options
        
        if options != "":
            command = command + space
            
        command = command + self._output
        
        return command
    
    def visit_program_node(self, node):
        self._program = node.path
    
    def visit_input_file_node(self, node):
        self._inputs.append({ "options": copy.deepcopy(self._tempInputOptionsMap), "path": node.path })
        self._tempInputOptionsMap = {}
    
    def visit_output_file_node(self, node):
        self._output = node.path
        
    def visit_configuration_node(self, node):
        if node.x != None and node.y != None:
            self._options["-s"] = str(node.x) + "x" + str(node.y)
        if node.fps != None:
            self._options["-r"] = str(node.fps)
            
    def visit_range_node(self, node):
        if node.start != None:
            self._options["-ss"] = str(node.start)
        if node.duration != None:
            self._options["-t"] = str(node.duration)

    def visit_image_node(self, node):
        self._tempInputOptionsMap["-loop"] = "1"
        self._options["-shortest"] = ""
        self._inputs.append({ "options": copy.deepcopy(self._tempInputOptionsMap), "path": node.path })
        self._tempInputOptionsMap = {}

    def visit_silence_node(self, node):
        self._options["-vn"] = ""


















