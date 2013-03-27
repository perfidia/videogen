#!/usr/bin/env python

from PIL import Image, ImageDraw, ImageFont

class Board(object):
    def __init__(self, filename, size, color):
        self._image = Image.new("RGB", size, color)
        self.filename = filename
        self._ctx = ImageDraw.Draw(self._image)
        
    def save(self):
        self._image.save(self.filename)
        
    def add_text(self, text, pos, color, font = "pilfonts/courO24.pil"):
        font = ImageFont.load(font)
        self._ctx.text(pos, text, color, font)
        
    def add_image(self, filename, size, pos = (0, 0)):
        img = Image.open(filename)
        im = img.resize(size)
        #3rd param is alpha mask
        self._image.paste(im, pos, im)

