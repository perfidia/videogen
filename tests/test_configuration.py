import unittest
from videogenlib import *

class TestConfiguration(unittest.TestCase):
    def setUp(self):
        self.root = ProgramNode("ffmpeg")
        self.input1 = InputFileNode("input1.avi")
        self.output = OutputFileNode("output.avi")
        self.root.add_child(self.input1)
        self.root.add_child(self.output)
        
    def test_whole_config(self):
        config = ConfigurationNode(640, 360, 30)
        self.output.add_child(config)
        
        v = FFMpegVisitor()
        self.root.accept(v)
        command = v.get_command()
        
        self.assertEqual("ffmpeg -i input1.avi -s 640x360 -r 30 output.avi", command, "test_whole_config")
        
    def test_resolution_config(self):
        config = ConfigurationNode(640, 360, None)
        self.output.add_child(config)
        
        v = FFMpegVisitor()
        self.root.accept(v)
        command = v.get_command()
        
        self.assertEqual("ffmpeg -i input1.avi -s 640x360 output.avi", command, "test_resolution_config")
        
    def test_fps_config(self):
        config = ConfigurationNode(None, None, 24)
        self.output.add_child(config)
        
        v = FFMpegVisitor()
        self.root.accept(v)
        command = v.get_command()
        
        self.assertEqual("ffmpeg -i input1.avi -r 24 output.avi", command, "test_fps_config")
        
    
    
if __name__ == "__main__":
    unittest.main()
    