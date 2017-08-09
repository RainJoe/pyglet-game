import sys
import pyglet
import random

from field import Field
sys.path.append('../')
from api import fillLine, fillRect, fillText, strokRect


#游戏窗口类
class Game(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super(Game, self).__init__(*args, **kwargs)
        self.field = Field(20, 30, 40)
        #初始化field
        for i in range(self.field.row):
            for j in range(self.field.col):
                if random.random() < 0.2:
                    self.field.field[i][j].reborn()

    def on_draw(self):
        #方格大小
        size = 20
        #初始化界面
        self.clear()
        fillRect(0, 0, self.width, self.height, (255, 255, 255))
        for i in range(self.field.row):
            for j in range(self.field.col):
                strokRect(j*size , i*size, size, size, (0, 0, 0))
        #画cell
        for i in range(self.field.row):
            for j in range(self.field.col):
                self.field.field[i][j].drawCell(i, j)

    def update(self, dt):
        for i in range(self.field.row):
            for j in range(self.field.col):
                numOfLive = 0
                cell = self.field.get(i, j)
                for n in self.field.get_nbr(i, j):
                    if n.isAlive():
                        numOfLive += 1
                if cell.isAlive():
                    if numOfLive < 2 or numOfLive > 3:
                        cell.die()
                elif numOfLive == 3:
                    cell.reborn()


if __name__ == "__main__":
    game = Game(width=800, height=600)
    #定时器
    pyglet.clock.schedule_interval(game.update, 1/60.)
    pyglet.app.run()
