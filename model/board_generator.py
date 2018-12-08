from random import sample
from tile import Tile
from utils import neighbours


class BoardGenerator:
    def __init__(self, size, numMines):
        self.numMines = numMines
        self.size = size
        self.board = []
        self.generate_board()

    def generate_board(self):
        # Generate a board for Minesweeper
        self.board = [[Tile(j, i) for i in range(0, self.size)] for j in range(0, self.size)]

        # select self.numMines random fields from 0 to self.size*self.size - 1
        fields_with_mines_ids = sample(range(0, self.size * self.size), self.numMines)

        # for a given field n select the field with coordinates (i,j) such that i*self.size + j = n
        fields_with_mines = map(lambda n, size=self.size: ((n - n % size) / size, n % size), fields_with_mines_ids)

        for field in fields_with_mines:
            i, j = field
            self.board[i][j].mine = True

            # add 1 to all neighbours of that field, except of the fields that already contain a bomb
            for (x, y) in neighbours(i, j, self.size):
                    if not self.board[x][y].mine:
                        self.board[x][y].neighbours_with_mines += 1
