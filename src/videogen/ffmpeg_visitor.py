#!/usr/bin/env python

from visitor import Visitor
from constants import *

import copy
import os

class FFMpegVisitor(Visitor):
    def __init__(self):
        self._program = ""
        self._inputs = []
        self._output = ""
        self._options = {}
        self._repeat_times = 0
        self._input_number = 0
        self._map_audio = False
        self._map_video = False
        
        self._tempInputOptionsMap = {}
    
    def get_command(self):
        space = " "
        inputs = ""
        
        if self._input_number > 1:
            self._options["-shortest"] = ""
        
        for input in self._inputs:
            inp = input["options"]
            
            for option in inp:
                inputs = inputs + space + option
                if inp[option] != "":
                    inputs = inputs + space + inp[option]
            
            if "path" in input:
                inputs = inputs + space + "-i" + space + input["path"]
            elif "color" in input:
                inputs = inputs + space + "-f lavfi -i" + space + "\"color=c=" + input["color"] + "\""
            
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
            
        if self._repeat_times > 1:
            (directory_name, file_name) = os.path.split(self._output)
            
            temp_file = directory_name + "\\DEADBEEF" + file_name
            command = command + temp_file
            
            repeat_command = self._program
            
            for i in range(0, self._repeat_times):
                repeat_command = repeat_command + " -i " + temp_file
                
            repeat_command = repeat_command + space + "-filter_complex \"concat=n=" + str(self._repeat_times)
            repeat_command = repeat_command + ":v=1:a=1 [v] [a]\" -map \"[v]\" -map \"[a]\""
            
            repeat_command = repeat_command + space + self._output
            
            command = command + space + "&&" + space + repeat_command
        else:
            command = command + self._output
        
        return command
    
    def visit_program_node(self, node):
        self._program = node.path
    
    def visit_input_file_node(self, node):
        if self._map_audio == True:
            type = 0
            if node.type == TYPE_VIDEO:
                type = 1
            elif node.type == TYPE_AUDIO:
                type = 0
            self._options["-map " + str(self._input_number) + ":" + str(type)] = ""
            self._map_audio = False
        if self._map_video == True:
            type = 0
            if node.type == TYPE_VIDEO:
                type = 0
            self._options["-map " + str(self._input_number) + ":" + str(type)] = ""
            self._map_video = False
        
        self._inputs.append({ "options": copy.deepcopy(self._tempInputOptionsMap), "path": node.path })
        self._tempInputOptionsMap = {}
        
        self._input_number = self._input_number + 1
    
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
        if self._map_audio == True:
            type = 0
            if node.type == TYPE_VIDEO:
                type = 1
            elif node.type == TYPE_AUDIO:
                type = 0
            self._options["-map " + str(self._input_number) + ":" + str(type)] = ""
            self._map_audio = False
        if self._map_video == True:
            type = 0
            if node.type == TYPE_VIDEO:
                type = 0
            self._options["-map " + str(self._input_number) + ":" + str(type)] = ""
            self._map_video = False
            
        self._tempInputOptionsMap["-loop"] = "1"
        self._options["-shortest"] = ""
        self._inputs.append({ "options": copy.deepcopy(self._tempInputOptionsMap), "path": node.path })
        self._tempInputOptionsMap = {}
        self._input_number = self._input_number + 1

    def visit_silence_node(self, node):
        self._options["-vn"] = ""
        
    def visit_repeat_node(self, node):
        self._repeat_times = node.times
        
    def visit_color_node(self, node):
        if self._map_audio == True:
            type = 0
            if node.type == TYPE_VIDEO:
                type = 1
            elif node.type == TYPE_AUDIO:
                type = 0
            self._options["-map " + str(self._input_number) + ":" + str(type)] = ""
            self._map_audio = False
        if self._map_video == True:
            type = 0
            if node.type == TYPE_VIDEO:
                type = 0
            self._options["-map " + str(self._input_number) + ":" + str(type)] = ""
            self._map_video = False
            
        self._inputs.append({ "options": copy.deepcopy(self._tempInputOptionsMap), "color": node.color })
        self._tempInputOptionsMap = {}
        self._input_number = self._input_number + 1
        
    def visit_concat_node(self, node):
        pass
    
    def visit_audio_node(self, node):
        self._map_audio = True
        
    def visit_video_node(self, node):
        self._map_video = True
        


















