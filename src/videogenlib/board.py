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
        
    def add_image(self, filename, size, pos = (0, 0), is_transparent = 1):
        img = Image.open(filename)
        im = img.resize(size)
        #3rd param is alpha mask
        if is_transparent:
            self._image.paste(im, pos, im)
        else:
            self._image.paste(im, pos)

    def add_line(self, xy1, xy2, fill, width):
        self._ctx.line([xy1, xy2], fill, width)
    
    def add_rectangle(self, xy1, xy2, fill):
        self._ctx.rectangle([xy1, xy2], fill)
        
    def add_ellipse(self, xy1, xy2, fill):
        self._ctx.ellipse((xy1[0], xy1[1], xy2[0], xy2[1]), fill)
        
        
        