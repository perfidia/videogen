#!/usr/bin/env python

from ffmpeg_visitor import FFMpegVisitor
from program_node import ProgramNode
from input_file_node import InputFileNode
from output_file_node import OutputFileNode
from configuration_node import ConfigurationNode

def main():
    visitor = FFMpegVisitor()
    
    root = ProgramNode("ffmpeg")
    root.add_child(InputFileNode("mov.avi"))
    root.add_child(InputFileNode("mov2.avi"))
    out = OutputFileNode("out.avi")
    out.add_child(ConfigurationNode(800, 600, 24))
    
    root.add_child(out)
    
    root.accept(visitor)
    
    print visitor.get_command()
    
    return

if __name__ == "__main__":
    main()