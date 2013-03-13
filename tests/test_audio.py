import unittest
from videogen import *

class TestAudio(unittest.TestCase):
    def setUp(self):
        self.root = ProgramNode("ffmpeg")
        self.output = OutputFileNode("output.avi")
        self.root.add_child(self.output)               
        
    def test_color(self):
        colorInput = ColorNode("#4444DD")
        self.root.add_child(colorInput)
        self.output.add_child(RepeatNode(2))
        
        v = FFMpegVisitor()
        self.root.accept(v)
        command = v.get_command()
        print command
        
        #self.assertEqual("ffmpeg -i input1.avi -ss 10 output.avi", command, "test_resolution_config")
        
    def test_audio_from_video(self):
        colorInput = ColorNode("#4444DD")
        self.root.add_child(colorInput)
        videoInput = InputFileNode("video.mp4", TYPE_VIDEO)
        self.root.add_child(videoInput)
        videoInput.add_child(AudioNode())
        colorInput.add_child(VideoNode())
        
        
        v = FFMpegVisitor()
        self.root.accept(v)
        command = v.get_command()
        print command
        
    
    
if __name__ == "__main__":
    unittest.main()
    