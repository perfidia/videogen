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
        self._program = self._options.encoder
        
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
                        units = None
                        start = None
                        end = None
                        
                        for i in effect.getElementsByTagName("unit"):
                            units = i.firstChild.data
                            print units
                        
                        for i in effect.getElementsByTagName("from"):
                                start = i.firstChild.data.strip()
                                print start
                        for i in effect.getElementsByTagName("to"):
                                end = i.firstChild.data.strip()
                                print end
                                
                        range = RangeNode(start, self.calculate_length(start, end, units))
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


    def calculate_length(self, start, end, units):
        if units == "s":         
            return int(end)-int(start)
        elif units == "m":
            return (int(end)-int(start))*60
        elif units == "m:s":
            startTemp = start.split(":")
            startMinutes = int(startTemp[0])
            startSeconds = int(startTemp[1]) + startMinutes*60
            print startSeconds
            endTemp = end.split(":")
            endMinutes = int(endTemp[0])
            endSeconds = int(endTemp[1])+endMinutes*60 
            print endSeconds
            return endSeconds - startSeconds
            

             
























