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
        self._concat = False
        self._is_image = False
        self._is_color = False
        self._sar = 0
        self._video_codec = "libx264"
        self._audio_codec = "libmp3lame"
        
        self._tempInputOptionsMap = {}
    
    def get_command(self):
        space = " "
        inputs = ""
        
        concat = "";
        
        if self._input_number > 1:
            self._options["-shortest"] = ""
            
        if self._concat == True:
            concat = "-filter_complex \"concat=n=" + str(self._input_number)
            concat = concat + ":v=1:a=1 [v] [a]\" -map \"[v]\" -map \"[a]\""
        
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
            
        (directory_name, file_name) = os.path.split(self._output)
        temp_file = directory_name + os.sep + "DEADBEEF" + file_name
        temp_file2 = directory_name + os.sep + "DEADBEEF__DEADBEEF" + file_name
            
        if self._is_image == True or self._is_color == True:
            command = command + temp_file2
            another_command = space + "&&" + space + self._program + space
            another_command = another_command + "-i" + space + temp_file2 + space
            another_command = another_command + "-vf setsar=" + self._sar + space
            
            if "-y" in self._options:
                another_command = another_command + space + "-y" + space
                
            command = command + another_command
            
        if self._repeat_times > 1:
            command = command + temp_file
            
            repeat_command = self._program
            
            for i in range(0, self._repeat_times):
                repeat_command = repeat_command + " -i " + temp_file
                
            repeat_command = repeat_command + space + "-filter_complex \"concat=n=" + str(self._repeat_times)
            repeat_command = repeat_command + ":v=1:a=1 [v] [a]\" -map \"[v]\" -map \"[a]\""
            repeat_command = repeat_command + space + "-preset slow -minrate 800 -c:v " + self._video_codec
            
            if "-y" in self._options:
                repeat_command = repeat_command + space + "-y"
            
            repeat_command = repeat_command + space + self._output
            
            command = command + space + "&&" + space + repeat_command
        else:
            if concat == "":
                command = command + self._output
            else:
                command = command + concat + space + self._output
        
        return command
    
    def visit_program_node(self, node):
        self._program = node.path
        
        self._options["-preset"] = "slow"
        #self._options["-crf"] = "10"
        self._options["-minrate"] = "800"
        self._options["-c:v"] = self._video_codec
        
        #self._options["-qmin"] = "40"
        #self._options["-qmax"] = "50"
        
        if node.overwrite == True:
            self._options["-y"] = ""
    
    def visit_input_file_node(self, node):
        print node.path
        print "map audio: " + str(self._map_audio)
        print "map video: " + str(self._map_video)
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
            self._options["-vf setsar="+str(node.sar)] = ""
            self._sar = str(node.sar)
        if node.fps != None:
            self._options["-r"] = str(node.fps)
            
        self._audio_codec = node.audio_codec
        self._video_codec = node.video_codec
            
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
        self._is_image = True

    def visit_silence_node(self, node):
        #self._options["-an"] = ""
        self._tempInputOptionsMap["-f"] = "lavfi"
        self._inputs.append({ "options": copy.deepcopy(self._tempInputOptionsMap), "path": "aevalsrc=0" })
        self._tempInputOptionsMap = {}
        self._options["-map " + str(self._input_number) + ":0"] = ""
        self._input_number = self._input_number + 1
        
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
        self._is_color = True
        
    def visit_concat_node(self, node):
        self._concat = True
    
    def visit_audio_node(self, node):
        self._map_audio = True
        
    def visit_video_node(self, node):
        self._map_video = True
        


















