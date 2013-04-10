#!/usr/bin/env python

import copy
import os
from xml.dom import minidom
from videogenlib import *
from constants import *
from video_node import VideoNode
from audio_node import AudioNode
from color_node import ColorNode
from board import Board

class ShotsTrees(object):
    def __init__(self, options):
        self._options = copy.deepcopy(options)
        self._dom = None
        self._board_num = 0
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
            
        return (shots, configuration_node)
    
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
                
                for i in effect.getElementsByTagName("from"):
                        start = i.firstChild.data.strip()
                for i in effect.getElementsByTagName("to"):
                        end = i.firstChild.data.strip()
                        
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
                
        for board in image.getElementsByTagName("board"):
            filename = self._parse_image_board(board)
            image_input = ImageNode(filename)
            image_input.add_child(VideoNode())
            shot.add_child(image_input)
        
    def _parse_image_board(self, board):
        filename =  self._options.tmp + self._options.attach + "DEADBEEF__board" + str(self._board_num) + ".png"
        self._boardNum = self._board_num + 1
        x = 400
        y = 400
        bg_color = "#004444"
        element_coords = [  ]
        
        for configuration in board.getElementsByTagName("configuration"):
            for size in configuration.getElementsByTagName("size"):
                for width in size.getElementsByTagName("width"):
                    x = int(width.firstChild.data.strip())
                for height in size.getElementsByTagName("height"):
                    y = int(height.firstChild.data.strip())
                    
            for background in configuration.getElementsByTagName("background"):
                for color in background.getElementsByTagName("color"):
                    bg_color = color.firstChild.data.strip()
                    
        cBoard = Board(filename, (x, y), bg_color)
                    
        for text in board.getElementsByTagName("text"):
            text_content = ""
            text_pos_x = 0
            text_pos_y = 0
            text_color = "#FFFFFF"
            text_font = "pilfonts/courO24.pil"
            text_id = ""
            align_x = "FREE"
            align_y = "FREE"
            align_id = ""
            
            for content in text.getElementsByTagName("content"):
                text_content = content.firstChild.data.strip()
            
            for color in text.getElementsByTagName("color"):
                text_color = color.firstChild.data.strip()
                
            for idn in text.getElementsByTagName("id"):
                text_id = idn.firstChild.data.strip()
                
            for idn in text.getElementsByTagName("align_id"):
                align_id = idn.firstChild.data.strip()
                
            for fnt in text.getElementsByTagName("font"):
                text_font = fnt.firstChild.data.strip()
                
            for point in text.getElementsByTagName("point"):
                for px in text.getElementsByTagName("x"):
                    text_pos_x = int(px.firstChild.data.strip())
                for py in text.getElementsByTagName("y"):
                    text_pos_y = int(py.firstChild.data.strip())
                    
            for point in text.getElementsByTagName("align"):
                for px in point.getElementsByTagName("x"):
                    align_x = px.firstChild.data.strip()
                for py in point.getElementsByTagName("y"):
                    align_y = py.firstChild.data.strip()
                    
            text_size = cBoard.text_size(text_content, text_font)
            text_map = {
                        "type" : "text", 
                        "content" : text_content,
                        "color" : text_color,
                        "x" : text_pos_x,
                        "y" : text_pos_y,
                        "w" : text_size[0],
                        "h" : text_size[1],
                        "id" : text_id,
                        "font" : text_font,
                        "align_x" : align_x,
                        "align_y" : align_y,
                        "align_id" : align_id,
                        }
            
            element_coords.append(text_map)
            
            #cBoard.add_text(text_content, ( text_pos_x, text_pos_y), text_color)
            
        for picture in board.getElementsByTagName("picture"):
            pic_filename = ""
            pic_pos_x = 0
            pic_pos_y = 0
            pic_x = 100
            pic_y = 100
            is_transparent = 0
            pic_id = ""
            align_x = "FREE"
            align_y = "FREE"
            align_id = ""
            
            
            for load in picture.getElementsByTagName("filename"):
                pic_filename = load.firstChild.data.strip()
                
            for point in picture.getElementsByTagName("point"):
                for px in point.getElementsByTagName("x"):
                    pic_pos_x = int(px.firstChild.data.strip())
                for py in point.getElementsByTagName("y"):
                    pic_pos_y = int(py.firstChild.data.strip())
                    
            for idn in picture.getElementsByTagName("id"):
                pic_id = idn.firstChild.data.strip()
                
            for idn in picture.getElementsByTagName("align_id"):
                align_id = idn.firstChild.data.strip()
                    
            for size in picture.getElementsByTagName("size"):
                for px in size.getElementsByTagName("x"):
                    pic_x = int(px.firstChild.data.strip())
                for py in size.getElementsByTagName("y"):
                    pic_y = int(py.firstChild.data.strip())
                    
            for transparent in picture.getElementsByTagName("transparent"):
                is_transparent = int(transparent.firstChild.data.strip())
                
            for point in picture.getElementsByTagName("align"):
                for px in point.getElementsByTagName("x"):
                    align_x = px.firstChild.data.strip()
                for py in point.getElementsByTagName("y"):
                    align_y = py.firstChild.data.strip()

            image_map = {
                         "type" : "image",
                         "filename" : self._conf_dir + pic_filename,
                         "w" : pic_x,
                         "h" : pic_y,
                         "x" : pic_pos_x,
                         "y" : pic_pos_y,
                         "transparent" : is_transparent == 1,
                         "id" : pic_id,
                         "align_x" : align_x,
                         "align_y" : align_y,
                         "align_id" : align_id,
                         }
            
            element_coords.append(image_map)
                    
            #cBoard.add_image(self._conf_dir + pic_filename, 
            #                 (pic_x, pic_y), 
            #                 ( pic_pos_x, pic_pos_y),
            #                 is_transparent == 1)
            
        for line in board.getElementsByTagName("line"):
            pos_x1 = 0
            pos_y1 = 0
            pos_x2 = 0
            pos_y2 = 0
            line_color = "#FFFFFF"
            line_width = 1
            line_id = ""
            align_x = "FREE"
            align_y = "FREE"
            align_id = ""
                
            for point in line.getElementsByTagName("point_start"):
                for px in point.getElementsByTagName("x"):
                    pos_x1 = int(px.firstChild.data.strip())
                for py in point.getElementsByTagName("y"):
                    pos_y1 = int(py.firstChild.data.strip())

            
            for point in line.getElementsByTagName("point_end"):
                for px in point.getElementsByTagName("x"):
                    pos_x2 = int(px.firstChild.data.strip())
                for py in point.getElementsByTagName("y"):
                    pos_y2 = int(py.firstChild.data.strip())
                    
            for idn in line.getElementsByTagName("id"):
                line_id = idn.firstChild.data.strip()
                
            for idn in line.getElementsByTagName("width"):
                line_width = int(idn.firstChild.data.strip())
                
            for idn in line.getElementsByTagName("align_id"):
                align_id = idn.firstChild.data.strip()
                    
            for color in line.getElementsByTagName("color"):
                line_color = color.firstChild.data.strip()
                
            for point in line.getElementsByTagName("align"):
                for px in point.getElementsByTagName("x"):
                    align_x = px.firstChild.data.strip()
                for py in point.getElementsByTagName("y"):
                    align_y = py.firstChild.data.strip()

            image_map = {
                         "type" : "line",
                         "width" : line_width,
                         "x1" : pos_x1,
                         "y1" : pos_y1,
                         "x2" : pos_x2,
                         "y2" : pos_y2,
                         "color" : line_color,
                         "id" : line_id,
                         "align_x" : align_x,
                         "align_y" : align_y,
                         "align_id" : align_id,
                         }
            
            element_coords.append(image_map)
            
        for rectangle in board.getElementsByTagName("rectangle"):
            pos_x1 = 0
            pos_y1 = 0
            pos_x2 = 0
            pos_y2 = 0
            rectangle_color = "#FFFFFF"
            rectangle_id = ""
            align_x = "FREE"
            align_y = "FREE"
            align_id = ""
                
            for point in rectangle.getElementsByTagName("point_start"):
                for px in point.getElementsByTagName("x"):
                    pos_x1 = int(px.firstChild.data.strip())
                for py in point.getElementsByTagName("y"):
                    pos_y1 = int(py.firstChild.data.strip())
                    
            
            for point in rectangle.getElementsByTagName("point_end"):
                for px in point.getElementsByTagName("x"):
                    pos_x2 = int(px.firstChild.data.strip())
                for py in point.getElementsByTagName("y"):
                    pos_y2 = int(py.firstChild.data.strip())
                    
            for idn in rectangle.getElementsByTagName("id"):
                rectangle_id = idn.firstChild.data.strip()
                
            for idn in rectangle.getElementsByTagName("align_id"):
                align_id = idn.firstChild.data.strip()
                    
            for color in rectangle.getElementsByTagName("color"):
                rectangle_color = color.firstChild.data.strip()
                
            for point in rectangle.getElementsByTagName("align"):
                for px in point.getElementsByTagName("x"):
                    align_x = px.firstChild.data.strip()
                for py in point.getElementsByTagName("y"):
                    align_y = py.firstChild.data.strip()

            image_map = {
                         "type" : "rectangle",
                         "x1" : pos_x1,
                         "y1" : pos_y1,
                         "x2" : pos_x2,
                         "y2" : pos_y2,
                         "color" : rectangle_color,
                         "id" : rectangle_id,
                         "align_x" : align_x,
                         "align_y" : align_y,
                         "align_id" : align_id,
                         }
            
            element_coords.append(image_map)
            
        for ellipse in board.getElementsByTagName("ellipse"):
            pos_x1 = 0
            pos_y1 = 0
            pos_x2 = 0
            pos_y2 = 0
            ellipse_color = "#FFFFFF"
            ellipse_id = ""
            align_x = "FREE"
            align_y = "FREE"
            align_id = ""
                
            for point in ellipse.getElementsByTagName("point_start"):
                for px in point.getElementsByTagName("x"):
                    pos_x1 = int(px.firstChild.data.strip())
                for py in point.getElementsByTagName("y"):
                    pos_y1 = int(py.firstChild.data.strip())
                    
            
            for point in ellipse.getElementsByTagName("point_end"):
                for px in point.getElementsByTagName("x"):
                    pos_x2 = int(px.firstChild.data.strip())
                for py in point.getElementsByTagName("y"):
                    pos_y2 = int(py.firstChild.data.strip())
                    
            for idn in ellipse.getElementsByTagName("id"):
                ellipse_id = idn.firstChild.data.strip()
                
            for idn in ellipse.getElementsByTagName("align_id"):
                align_id = idn.firstChild.data.strip()
                
            for point in ellipse.getElementsByTagName("align"):
                for px in point.getElementsByTagName("x"):
                    align_x = px.firstChild.data.strip()
                for py in point.getElementsByTagName("y"):
                    align_y = py.firstChild.data.strip()
                    
            for color in ellipse.getElementsByTagName("color"):
                ellipse_color = color.firstChild.data.strip()

            image_map = {
                         "type" : "ellipse",
                         "x1" : pos_x1,
                         "y1" : pos_y1,
                         "x2" : pos_x2,
                         "y2" : pos_y2,
                         "color" : ellipse_color,
                         "id" : ellipse_id,
                         "align_x" : align_x,
                         "align_y" : align_y,
                         "align_id" : align_id,
                         }
            
            element_coords.append(image_map)
            
        for element in element_coords:
            if element["align_id"] != "":
                x, y = self._calculate_position(element["align_id"], element_coords, element["align_x"], element["align_y"])
                if "__finite_coords" not in element:
                    element["__finite_coords"] = True
                    if "x" in element and "y" in element:
                        element["x"] = element["x"] + x
                        element["y"] = element["y"] + y
                    if "x1" in element and "y1" in element and "x2" in element and "y2" in element:
                        element["x1"] = element["x1"] + x
                        element["y1"] = element["y1"] + y
                        element["x2"] = element["x2"] + x
                        element["y2"] = element["y2"] + y
            
        for element in element_coords:
            if element["type"] == "text": 
                cBoard.add_text(element["content"], ( element["x"], element["y"]), element["color"], element["font"])
            elif element["type"] == "image":
                cBoard.add_image(element["filename"], 
                                 (element["w"], element["h"]), 
                                 ( element["x"], element["y"]),
                                 element["transparent"])
            elif element["type"] == "line":
                cBoard.add_line((element["x1"], element["y1"]), 
                                (element["x2"], element["y2"]),
                                element["color"],
                                element["width"])
            elif element["type"] == "rectangle":
                cBoard.add_rectangle((element["x1"], element["y1"]), 
                                (element["x2"], element["y2"]),
                                element["color"])
            elif element["type"] == "ellipse":
                cBoard.add_ellipse((element["x1"], element["y1"]), 
                                (element["x2"], element["y2"]),
                                element["color"])
        
        cBoard.save()
        return filename
    
    def _position_coords(self, x1, y1, x2, y2, coord_type, align_x = "FREE", align_y = "FREE"):
        if coord_type == 0:
            x2 = x2+x1
            y2 = y2+y1
        
        out_x = 0
        out_y = 0
        
        if align_x.upper() == "LEFT" or align_x.upper() == "FREE":
            out_x = x1
        elif align_x.upper() == "RIGHT":
            out_x = x2
        elif align_x.upper() == "CENTER":
            out_x = int((x1+x2)/2)
            
        if align_y.upper() == "TOP" or align_y.upper() == "FREE":
            out_y = y1
        elif align_y.upper() == "BOTTOM":
            out_y = y2
        elif align_y.upper() == "CENTER":
            out_y = int((y1+y2)/2)
            
        return out_x, out_y
    
    def _calculate_position(self, element_id, elements, align_x = "FREE", align_y = "FREE"):
        
        for element in elements:
            if element["id"] == element_id:
                if "__finite_coords" in element:
                    if "x" in element and "y" in element:
                        return self._position_coords(element["x"], element["y"], 
                                                     element["w"], element["h"],
                                                     0, align_x, align_y);
                    if "x1" in element and "y1" in element:
                        return self._position_coords(element["x1"], element["y1"], 
                                                     element["x2"], element["y2"],
                                                     1, align_x, align_y);
                else:
                    if element["align_id"] != "":
                        if "x" in element and "y" in element:
                            x, y = self._calculate_position(element["align_id"], elements, element["align_x"], element["align_y"])
                            element["x"] = element["x"] + x
                            element["y"] = element["y"] + y
                            element["__finite_coords"] = True
                            return self._position_coords(element["x"], element["y"], 
                                                         element["w"], element["h"],
                                                         0, align_x, align_y);
                        
                        if "x1" in element and "y1" in element and "x2" in element and "y2" in element:
                            x, y = self._calculate_position(element["align_id"], elements, element["align_x"], element["align_y"])
                            element["x1"] = element["x1"] + x
                            element["y1"] = element["y1"] + y
                            element["x2"] = element["x2"] + x
                            element["y2"] = element["y2"] + y
                            element["__finite_coords"] = True
                            return self._position_coords(element["x1"], element["y1"], 
                                                         element["x2"], element["y2"],
                                                         1, align_x, align_y);
                    else:
                        element["__finite_coords"] = True
                        if "x" in element and "y" in element:
                            return self._position_coords(element["x"], element["y"], 
                                                         element["w"], element["h"],
                                                         0, align_x, align_y);
                        if "x1" in element and "y1" in element:
                            return self._position_coords(element["x1"], element["y1"], 
                                                         element["x2"], element["y2"],
                                                         1, align_x, align_y);
        
        return 0, 0

    def get_configuration_node(self):
        width = None
        height = None
        fps = None
        sar = -1
        video_codec = "libx264"
        audio_codec = "libmp3lame"
        subs = None
        
        for node in self._dom.getElementsByTagName("configuration"):
            for frame in node.getElementsByTagName("frame"):
                for i in frame.getElementsByTagName("width"):
                    width = int(i.firstChild.data.strip())
                for i in frame.getElementsByTagName("height"):
                    height = int(i.firstChild.data.strip())
                for i in frame.getElementsByTagName("sar"):
                    sar = float(i.firstChild.data.strip())
            for rate in node.getElementsByTagName("rate"):
                fps = int(rate.firstChild.data.strip())
            for codecs in node.getElementsByTagName("codecs"):
                for v in codecs.getElementsByTagName("video"):
                    for k in v.getElementsByTagName("key"):
                        video_codec = k.firstChild.data.strip()
                for a in codecs.getElementsByTagName("audio"):
                    for k in a.getElementsByTagName("key"):
                        audio_codec = k.firstChild.data.strip()
            for subtitles in node.getElementsByTagName("subtitles"):
                subs = subtitles.firstChild.data.strip()
            
        configuration_node = ConfigurationNode(width, height, fps, sar,
                                               video_codec, audio_codec, subs)
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
            #print startSeconds
            endTemp = end.split(":")
            endMinutes = int(endTemp[0])
            endSeconds = int(endTemp[1])+endMinutes*60 
            #print endSeconds
            return endSeconds - startSeconds
            

             
























