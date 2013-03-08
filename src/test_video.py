import unittest
from videogen import *

class TestConfiguration(unittest.TestCase):
    def setUp(self):
        self.root = ProgramNode("ffmpeg")
        self.input1 = InputFileNode("input1.avi")
        self.output = OutputFileNode("output.avi")
        self.root.add_child(self.input1)
        self.root.add_child(self.output)
        
    def test_range_from_to(self):
        range = RangeNode(10, 20)
        self.output.add_child(range)
        
        v = FFMpegVisitor()
        self.root.accept(v)
        command = v.get_command()
        
        self.assertEqual("ffmpeg  -i input1.avi  -ss 10 -t 20 output.avi", command, "test_whole_config")
        
    def test_range_from(self):
        range = RangeNode(10, None)
        self.output.add_child(range)
        
        v = FFMpegVisitor()
        self.root.accept(v)
        command = v.get_command()
        
        self.assertEqual("ffmpeg  -i input1.avi  -ss 10 output.avi", command, "test_resolution_config")
        
    def test_fps_config(self):
        range = RangeNode(None, 30)
        self.output.add_child(range)
        
        v = FFMpegVisitor()
        self.root.accept(v)
        command = v.get_command()
        
        self.assertEqual("ffmpeg  -i input1.avi  -t 30 output.avi", command, "test_fps_config")
        
    
    
if __name__ == "__main__":
    unittest.main()
    