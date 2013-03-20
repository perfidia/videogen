#!/usr/bin/env python

import copy
import os
from xml.dom import minidom
from videogen import *
from constants import *
from video_node import VideoNode
from audio_node import AudioNode
from color_node import ColorNode

class ShotsTrees(object):
    def __init__(self, options):
        self._options = copy.deepcopy(options)
        self._dom = None
        if self._options.conf != None:
            self._dom = minidom.parse(self._options.conf)
            self._conf_dir = os.path.dirname(os.path.abspath(self._options.conf)) + os.sep
        self._program = self._options.encoder
        
    def create(self):
        if self._dom == None:
            return []
        
        shots = []
        num = 0
        
        configuration_node = self.get_configuration_node()
        
        for node in self._dom.getElementsByTagName("shot"):
            shot = ProgramNode(self._program)
            shot.overwrite = self._options.overwrite
            num = num + 1
            temp_output = OutputFileNode(self._options.tmp + self._options.attach + str(num)+".avi")
            temp_output.add_child(configuration_node)
            shot.add_child(temp_output)
            
            for video in node.getElementsByTagName("video"):
                self._parse_video(video, shot, temp_output)
                
            for audio in node.getElementsByTagName("audio"):
                self._parse_audio(audio, shot, temp_output)
                
            for image in node.getElementsByTagName("image"):
                self._parse_image(image, shot, temp_output)
            
            shots.append(shot)
            
        return shots
    
    def _parse_video(self, video, shot, temp_output):
        video_input = None
        for load in video.getElementsByTagName("load"):
            for filename in load.childNodes:
                if load.getAttributeNode("type").nodeValue.strip() == "AudioVideoFile":
                    video_input = InputFileNode(self._conf_dir + filename.data.strip(), TYPE_VIDEO)
                    video_input.add_child(VideoNode())
                    video_input.add_child(AudioNode())
                    shot.add_child(video_input)
                elif load.getAttributeNode("type").nodeValue.strip() == "VideoFile":
                    video_input = InputFileNode(self._conf_dir + filename.data.strip(), TYPE_VIDEO)
                    video_input.add_child(VideoNode())
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
                        
                zero = "0"
                if units == "m:s":
                    zero = "0:0"
                range = RangeNode(self.calculate_length(zero, start, units), 
                                  self.calculate_length(start, end, units))
                temp_output.add_child(range)
            
            elif attr == "VideoRepeat":
                times = 0
                for i in effect.getElementsByTagName("times"):
                    for j in i.childNodes:
                        times = j.data.strip()
                        
                repeat = RepeatNode(int(times))
                temp_output.add_child(repeat)
                
    def _parse_audio(self, audio, shot, temp_output):
        audio_input = None
        for load in audio.getElementsByTagName("load"):
            for filename in load.childNodes:
                if filename.nodeType == filename.TEXT_NODE:
                    audio_input = None
                    if load.getAttributeNode("type").nodeValue.strip() == "AudioFile":
                        audio_input = InputFileNode(self._conf_dir + filename.data.strip(), TYPE_AUDIO)
                        audio_input.add_child(AudioNode())
                    elif load.getAttributeNode("type").nodeValue.strip() == "VideoFile":
                        audio_input = InputFileNode(self._conf_dir + filename.data.strip(), TYPE_VIDEO)
                        audio_input.add_child(AudioNode())
                        
                    shot.add_child(audio_input)
                    
        for params in audio.getElementsByTagName("generate"):
            units = None
            duration = None
            
            for i in params.getElementsByTagName("unit"):
                units = i.firstChild.data
            
            for i in params.getElementsByTagName("duration"):
                duration = i.firstChild.data.strip()
                    
            silence = SilenceNode()
            range = RangeNode(0, self.calculate_length("0", duration, units))
            temp_output.add_child(range)
            temp_output.add_child(silence)
        
        for effect in audio.getElementsByTagName("effect"):
            attr = effect.getAttributeNode("type").nodeValue
            
            if attr == "AudioRange":
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
                        
                zero = "0"
                if units == "m:s":
                    zero = "0:0"
                        
                range = RangeNode(self.calculate_length(zero, start, units), 
                                  self.calculate_length(start, end, units))
                temp_output.add_child(range)
            
            elif attr == "AudioRepeat":
                times = 0
                for i in effect.getElementsByTagName("times"):
                    for j in i.childNodes:
                        times = j.data.strip()
                        
                repeat = RepeatNode(int(times))
                temp_output.add_child(repeat)
                
    def _parse_image(self, image, shot, temp_output):
        image_input = None
        for load in image.getElementsByTagName("load"):
            for filename in load.childNodes:
                if filename.nodeType == filename.TEXT_NODE:
                    image_input = ImageNode(self._conf_dir + filename.data.strip())
                    image_input.add_child(VideoNode())
                    shot.add_child(image_input)
                    
        for generate in image.getElementsByTagName("generate"):
            for color in generate.getElementsByTagName("color"):
                color_input = ColorNode(color.firstChild.data.strip())
                color_input.add_child(VideoNode())
                shot.add_child(color_input)

    def get_configuration_node(self):
        width = None
        height = None
        fps = None
        
        for node in self._dom.getElementsByTagName("configuration"):
            for frame in node.getElementsByTagName("frame"):
                for i in frame.getElementsByTagName("width"):
                    width = int(i.firstChild.data.strip())
                for i in frame.getElementsByTagName("height"):
                    height = int(i.firstChild.data.strip())
            for rate in node.getElementsByTagName("rate"):
                fps = int(rate.firstChild.data.strip())
            
        configuration_node = ConfigurationNode(width, height, fps)
        return configuration_node

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
            

             
























