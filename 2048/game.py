import sys
import pyglet
from pyglet.window import key
from random import randrange, choice
import math
sys.path.append('../')
from api import fillRect, fillText, fillLine, strokRect
from gamemap import Field, Cell

#转置矩阵
def transpose(field):
    return [list(row) for row in zip(*field)]

#倒置矩阵
def invert(field):
    return [row[::-1] for row in field]


class Game(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(Game, self).__init__(*args, **kwargs)
        self.state = 'Init'
        self.win_value = 2048
        self.score = 0
        self.highscore = 0
        self.reset()

    def reset(self):
        if self.score > self.highscore:
            self.highscore = self.score
        self.score = 0
        self.field = Field(4, 4)
        self.spawn()
        self.spawn()

    def is_win(self):
        return any(any(i.card.val >= self.win_value for i in row) for row in \
            self.field.field)

    def is_gameover(self):
        actions = ['Left', 'Right', 'Up', 'Down']
        return not any(self.move_is_possible(move) for move in actions)

    def spawn(self):
        new_element = 4 if randrange(100) > 89 else 2
        try:
            (i, j) = choice([(i, j) for i in range(self.field.row) for \
                j in range(self.field.col) if self.field.field[i][j].card.val == 0])
            self.field.field[i][j].card = self.field.field[i][j].cards[int(math.log2(new_element))]
        except:
             self.state = 'Gameover'


    def move(self, direction):
        def move_row_left(row):
            def tighten(row): #把零散的非零单元挤到一块
                new_row = [i for i in row if i.card.val != 0]
                new_row += [Cell() for i in range(len(row) - len(new_row))]
                return new_row

            def merge(row):
                pair = False
                new_row = []
                for i in range(len(row)):
                    if pair: #如果有成对的则合并
                        c = Cell()
                        if (int(row[i].card.val)) == 0:
                            c.card = c.cards[0]
                        else:
                            c.card =  c.cards[int(math.log2(row[i].card.val)) + 1]
                        new_row.append(c)
                        self.score += c.card.val
                        pair = False
                    else:
                        if i + 1 < len(row) and row[i].card.val == row[i+1].card.val:
                            pair = True
                            c = Cell()
                            c.card = c.cards[0]
                            new_row.append(c)
                        else:
                            c = Cell()
                            if (int(row[i].card.val)) == 0:
                                c.card = c.cards[0]
                            else:
                                c.card = row[i].cards[int(math.log2(row[i].card.val))]
                            new_row.append(c)
                assert len(new_row) == len(row)
                return new_row
            return tighten(merge(tighten(row)))

        #利用转置，和倒置操作使代码量减少
        moves = {}
        moves['Left'] = lambda field: [move_row_left(row) for row in field]
        moves['Right'] = lambda field: invert(moves['Left'](invert(field)))
        moves['Up'] = lambda field: transpose(moves['Left'](transpose(field)))
        moves['Down'] = lambda field: transpose(moves['Right'](transpose(field)))

        if direction in moves:
            if self.move_is_possible(direction):
                self.field.field = moves[direction](self.field.field)
                self.spawn()
                return True
            else:
                return False

    def move_is_possible(self, direction):
        def row_is_left_movable(row):
            def change(i):
                if row[i].card.val == 0 and row[i + 1].card.val != 0:
                    return True
                if row[i].card.val != 0 and row[i+1].card.val == row[i].card.val:
                    return True
                return False
            return any(change(i)  for i in range(len(row) - 1))

        check = {}
        check['Left'] = lambda field: any(row_is_left_movable(row) for row in field)
        check['Right'] = lambda field: check['Left'](invert(field))
        check['Up'] = lambda field: check['Left']
        check['Down'] = lambda field: check['Right'](transpose(field))
        if direction in check:
            return check[direction](self.field.field)
        else:
            return False

    #监听键盘事件
    def on_key_press(self, symbol, modifiers):
        if self.state == 'Init':
            if symbol == key.K:
                self.state = 'Game'
            if symbol == key.R:
                self.reset()
        if self.state == 'Game':
            if symbol == key.A:
                self.move('Up')
            if symbol == key.D:
                self.move("Down")
            if symbol == key.W:
                self.move("Right")
            if symbol == key.S:
                self.move("Left")
            if symbol == key.Q:
                self.state = 'Init'
            if symbol == key.R:
                self.reset()
        if self.state == "Gameover":
            if symbol == key.Q:
                self.state = 'Init'
            if symbol == key.R:
                self.state = "Game"
                self.reset()
        if self.state == "Win":
            if symbol == key.Q:
                self.state = 'Init'
            if symbol == key.R:
                self.state = "Game"
                self.reset()

    def on_draw(self):
        if self.is_win():
            self.state = 'Win'

        if self.is_gameover():
            self.state = "Gameover"
        size = 100 #方格大小
        self.clear()
        fillRect(0, 0, self.width, self.height, (220,220,220))
        if self.state == 'Init':
            fillText("(K)Start", 200, 240, 16, (0, 0, 0, 255))
            fillText("(W)up (S)Down (A)Left (D)Right", 200, 220, 16, (0, 0, 0, 255))
            fillText("(R)Restart (Q)Exit", 200, 180, 20, (0, 0, 0, 255))
        if self.state == 'Game':
            fillRect(250, 430, 150, 50, (230,230,250))
            fillText("SCORE:%s" % self.score, 270 + 50, 405 + 50, 18, (105, 105, 105, 255))
            fillText("2048", 100, 455, 50, (139,69,19, 255))
            for i in range(self.field.row):
                for j in range(self.field.col):
                    self.field.field[i][j].drawCell(i, j)
        if self.state == 'Win':
            fillText("You Win", 200, 240, 16, (0, 0, 0, 255))
            fillText("(R)Restart (Q)Exit", 200, 180, 16, (0, 0, 0, 255))
        if self.state == 'Gameover':
            fillText("Game Over", 200, 240, 16, (0, 0, 0, 255))
            fillText("(R)Restart (Q)Exit", 200, 180, 16, (0, 0, 0, 255))

if __name__ == "__main__":
    game = Game(width=405, height=405+100)
    pyglet.app.run()
