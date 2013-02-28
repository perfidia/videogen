'''
Created on Feb 3, 2013

@author: Bartosz Alchimowicz
'''

class VideoGen(object):
	def __init__(self):
		self.configuration = None
		self.sequenct = None

class Configuration(object): pass
class Sequence(object): pass
class Shot(object): pass


class Element(object): pass
class Video(Element): pass
class Audio(Element): pass
class Image(Element): pass


class Action: pass

class LoadAction(Action): pass
class VideoFile(LoadAction): pass
class AudioFile(LoadAction): pass
class AudioStorageFile(LoadAction): pass
class ImageFile(LoadAction): pass

class GenerateAction(Action): pass
class BackgroundGenerate(GenerateAction): pass
class SileneceGenerate(GenerateAction): pass

class EffectAction(Action): pass
class VideoEffect(EffectAction): pass
class VideoRange(VideoEffect): pass
class VideoRepeat(VideoEffect): pass

class AudioEffect(EffectAction): pass
class AudioRange(AudioEffect): pass
class AudioRepeat(AudioEffect): pass

class ImageEffect(EffectAction): pass
