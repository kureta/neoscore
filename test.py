#!/usr/bin/env python3

from brown.core import brown
from brown.core.font import Font
from brown.core.text_object import TextObject
from brown.core.glyph import Glyph
from brown.core.path import Path
from brown.core.pen import Pen


brown.setup()


# Create music font
music_font = Font('gonville', 20)

glyph = Glyph(50, 50, '\uE118', music_font)
glyph.render()

path = Path(0, 0, Pen('#f29000'))

path.line_to(30, 40)
path.cubic_to(30, 40, 90, 60, 100, 100)
path.cubic_to(80, 80, 10, 120, 50, 75)
path.render()

line = Path.straight_line(50, 50, 50, 50)
line.render()

text = TextObject(80, 10, 'hello')
text.render()

brown.show()
