import pyglet

"""
Here are some functions which is like canvas api
"""

def fillText(text, x, y, font_size, color, font_name='Times New Roman'):
    label = pyglet.text.Label(text,
                          font_name=font_name,
                          font_size=font_size,
                          x=x, y=y,
                          anchor_x='center', anchor_y='center',
                          color=color)
    label.draw()

def fillRect(x, y, width, height, color):
    color_list = list(color) + list(color) + list(color) + list(color)
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
        ('v2i', (x, y, x+width, y, x+width, y+height, x, y+height)),
         ('c3B', tuple(color_list))
    )

def strokRect(x, y, width, height, color):
    color_list = list(color) + list(color) + list(color) + list(color)
    pyglet.graphics.draw(4, pyglet.gl.GL_LINE_LOOP,
        ('v2i', (x, y, x+width, y, x+width, y+height, x, y+height)),
        ('c3B', tuple(color_list))
    )

def fillLine(x1, y1, x2, y2, color):
    color_list = list(color) + list(color)
    pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
        ('v2i', (x1, y1, x2, y2)),
        ('c3B', tuple(color_list))
    )
