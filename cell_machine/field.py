from cell import Cell


#Field类
class Field:

    def __init__(self, size, row, col):
        self.row = row
        self.col = col
        self.field = [[Cell(size) for j in range(col)] for i in range(row)]

    def get(self, row, col):
        return self.field[row][col]

    def get_nbr(self, rown, coln):
        for m in range(3):
            for n in range(3):
                i = m - 1
                j = n - 1
                r = rown + i
                c = coln + j
                #判断邻居是否合法
                if (r > -1 and r < self.row and c > -1 and c < self.col and not \
                    (r == rown and c == coln)):
                    yield self.field[r][c]
