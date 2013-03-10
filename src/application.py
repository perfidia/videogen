#!/usr/bin/env python

from videogen import *
import os

def main():
    vidgen_parser = VideoGenOptionParser()
    options = vidgen_parser.get_options()
    
    trees = ShotsTrees(options)
    shots = trees.create()
    
    for shot in shots:
        visitor = FFMpegVisitor()
        shot.accept(visitor)
        command = visitor.get_command()
        print command
        os.system(command)
    
    
    '''
    root = ProgramNode("ffmpeg")
    root.add_child(InputFileNode("mov.avi"))
    root.add_child(InputFileNode("mov2.avi"))
    out = OutputFileNode("out.avi")
    out.add_child(ConfigurationNode(800, 600, 24))
    out.add_child(RangeNode(2, 10))
    root.add_child(ImageNode("ijo.png"))
    out.add_child(SilenceNode())
    out.add_child(RepeatNode(3))
    
    root.add_child(out)
    
    root.accept(visitor)
    
    print visitor.get_command()
    '''
        
    return

if __name__ == "__main__":
    main()
    