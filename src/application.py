#!/usr/bin/env python

from videogen import *

def main():
    visitor = FFMpegVisitor()
    
    root = ProgramNode("ffmpeg")
    root.add_child(InputFileNode("mov.avi"))
    root.add_child(InputFileNode("mov2.avi"))
    out = OutputFileNode("out.avi")
    out.add_child(ConfigurationNode(800, 600, 24))
    out.add_child(RangeNode(2, 10))
    root.add_child(ImageNode("ijo.png"))
    out.add_child(SilenceNode())
    
    root.add_child(out)
    
    root.accept(visitor)
    
    print visitor.get_command()
    
    return

if __name__ == "__main__":
    main()
    