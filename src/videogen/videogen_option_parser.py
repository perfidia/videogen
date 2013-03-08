#!/usr/bin/env python

from optparse import OptionParser

class VideoGenOptionParser(object):
    def __init__(self):
        self._parser = OptionParser()
        
        self._parser.add_option("-c", "--conf", help="input file in XML format", dest="conf")
        self._parser.add_option("-o", "--output", help="place where to generate output file (default is ./output.avi)", dest="output")
        self._parser.add_option("-t", "--tmp", help="directory for intermediate files (default is /tmp/)", dest="tmp")
        self._parser.add_option("-a", "--attach", help="a string which should be added before each file that is loaded", dest="attach")
        
        self._options = {}
        (self._options, args) = self._parser.parse_args()
        
        if self._options.output == None:
            self._options.output = "./output.avi"
            
        if self._options.tmp == None:
            self._options.tmp = "/tmp/"
            
        if self._options.attach == None:
            self._options.attach = ""
        
    def get_options(self):
        return self._options
    





















