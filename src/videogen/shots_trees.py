#!/usr/bin/env python

import copy
from xml.dom import minidom
from videogen import *

class ShotsTrees(object):
    def __init__(self, options):
        self._options = copy.deepcopy(options)
        self._dom = None
        if self._options.conf != None:
            self._dom = minidom.parse(self._options.conf)
        self._program = "ffmpeg"
        
    def create(self):
        if self._dom == None:
            return []
        
        shots = []
        num = 0
        
        for node in self._dom.getElementsByTagName("shot"):
            shot = ProgramNode(self._program)
            num = num + 1
            temp_output = OutputFileNode(self._options.tmp+str(num)+".avi")
            shot.add_child(temp_output)
            
            for video in node.getElementsByTagName("video"):
                video_input = None
                for load in video.getElementsByTagName("load"):
                    for filename in load.childNodes:
                        if filename.nodeType == filename.TEXT_NODE:
                            video_input = InputFileNode(filename.data.strip())
                            shot.add_child(video_input)
                
                for effect in video.getElementsByTagName("effect"):
                    attr = effect.getAttributeNode("type").nodeValue
                    
                    if attr == "VideoRange":
                        start = None
                        end = None
                        
                        for i in effect.getElementsByTagName("from"):
                            for j in i.childNodes:
                                start = j.data.strip()
                                
                        for i in effect.getElementsByTagName("to"):
                            for j in i.childNodes:
                                end = j.data.strip()
                                
                        range = RangeNode(start, end)
                        temp_output.add_child(range)
                    
                    elif attr == "VideoRepeat":
                        times = 0
                        for i in effect.getElementsByTagName("times"):
                            for j in i.childNodes:
                                times = j.data.strip()
                                
                        repeat = RepeatNode(int(times))
                        temp_output.add_child(repeat)
            
            shots.append(shot)
            
        return shots


























