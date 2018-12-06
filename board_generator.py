from random import sample


class BoardGenerator:
    def __init__(self, size, numMines):
        self.numMines = numMines
        self.size = size
        self.board = []
        self.generate_board()

    def generate_board(self):
        # Generate a board for minesweeper
        # A mine is represented by '-1'
        self.board = [[0 for i in range(0, self.size)] for j in range(0, self.size)]

        # select self.numMines random fields from 0 to self.size*self.size - 1
        fields_with_mines_ids = sample(range(0, self.size * self.size), self.numMines)

        # for a given field n selct the field with coordinates (i,j) such that i*self.size + j = n
        fields_with_mines = map(lambda n, size=self.size: ((n - n % size) / size, n % size), fields_with_mines_ids)

        for field in fields_with_mines:
            i, j = field
            self.board[i][j] = -1

            # add 1 to all neighbours of that field, except of the fields that already contain a bomb
            for x in range(max(0, i - 1), min(i + 2, self.size)):
                for y in range(max(0, j - 1), min(j + 2, self.size)):
                    if (x, y) != (i, j) and self.board[x][y] >= 0:
                        self.board[x][y] += 1