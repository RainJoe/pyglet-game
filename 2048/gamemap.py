import sys
sys.path.append('../')
from api import fillRect, fillText
import collections

Card = collections.namedtuple('Card', ['val', 'color', 'bcolor', 'tsize'])

class Cell:
    vals = [0, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
    colors = [(105, 105, 105, 255), (105, 105, 105, 255), (105, 105, 105, 255),
              (248,248,255, 255), (248,248,255, 255), (248,248,255, 255),
              (220,220,220, 255), (220,220,220, 255), (220,220,220, 255),
              (255,240,245, 255), (255,240,245, 255), (255,240,245, 255)]
    bcolors = [(216, 191, 216), (255,250,240), (255,222,173), (210,180,140),
              (244,164,96), (139,69,19), (188,143,143), (255,105,180),
              (139,0,139), (139,69,19), (128,0,0), (255,99,71),
              (255,140,0), (255,215,0), (184,134,11)]
    tsizes = [0, 80, 80, 80, 65, 65, 65, 45, 45, 45, 30, 30]
    def __init__(self):
        self.cards = [Card(val, color, bcolor, tsize) for val, color, bcolor, \
                      tsize in zip(self.vals, self.colors, self.bcolors, self.tsizes)]
        self.card = self.cards[0]

    def drawCell(self, i, j):
        if self.card.val != 0:
            fillRect(i*100+5 , j*100+5, 100-5, 100-5, self.card.bcolor)
            fillText(str(self.card.val), i*100 + 50, j*100 + 50, self.card.tsize, self.card.color)
        else:
            fillRect(i*100+5 , j*100+5, 100-5, 100-5, (205, 197, 191))

class Field:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.field = [[Cell() for j in range(col)] for i in range(row)]
