#!/usr/bin/env python
import os
import shutil
import subprocess

class SoftSubtitles(object):
    def __init__(self, output, subtitles):
        if output != None and subtitles != None:
            temp, temp0  = os.path.splitext(output)
            self.path = temp
            temp1, temp2 = os.path.splitext(subtitles)
            self.subtitles = temp1
            self.extension = temp2
        else:
            self.extension = None
            self.subtitles = None
            self.path = None
        
        
    def add_subtitles(self):
        if self.extension != None and self.path != None and self.subtitles != None:
            shutil.copyfile(self.subtitles+self.extension, self.path+self.extension)
            