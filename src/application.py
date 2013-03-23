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
        
    if shots:
        visitor = FFMpegVisitor()
        sequence = ProgramNode(options.encoder)
        sequence.overwrite = options.overwrite
        if len(shots) > 1:
            concat = ConcatNode()
            sequence.add_child(concat)
        sequence.add_child(OutputFileNode(options.output))
        
        i = 0
        
        for shot in shots:
            i = i + 1
            sequence.add_child(InputFileNode(options.tmp + str(i)+".avi", TYPE_VIDEO))
            
        sequence.accept(visitor)
        command = visitor.get_command()
        print command
        os.system(command)
        
    return

if __name__ == "__main__":
    main()
    