import sys
sys.path.append('../')
from api import fillRect


#Cell类
class Cell:

    def __init__(self, size):
        self.size = size
        self.alive = False

    def drawCell(self, i, j):
        if self.alive:
            fillRect(j*self.size, i*self.size, self.size, self.size, (0, 0, 0))

    def reborn(self):
        self.alive = True

    def isAlive(self):
        return self.alive

    def die(self):
        self.alive = False
