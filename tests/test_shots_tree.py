import unittest
from videogen import *

class Mock(object):
    def __init__(self):
        self.conf = ""
        pass
        
class TestConfiguration(unittest.TestCase):

    def setUp(self):
        options = Mock()
        options.conf = "/home/krawczo/git/videogen/configs/config1.xml"
        options.encoder ="/home/krawczo/ffmpeg/ffmpeg"
        options.temp = ""
        self.trees = ShotsTrees(options)

    def test_calculate_length_seconds(self):
        self.assertEqual(5, self.trees.calculate_length(3, 8, "s"), "test_calculate_length_seconds")
        
    def test_calculate_length_minutes(self):
        self.assertEqual(60, self.trees.calculate_length(1, 2, "m"), "test_calculate_length_minutes")
    
    def test_calculate_length_minutes_seconds(self):
        self.assertEqual(60, self.trees.calculate_length("1:30", "2:30", "m:s"), "test_calculate_length_minutes_seconds")
            
        
   
if __name__ == "__main__":
    unittest.main()
    