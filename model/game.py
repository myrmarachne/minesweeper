from bayesian_network import BayesianNetwork
from board_generator import BoardGenerator
from utils import neighbours


class Game:
    def __init__(self, size, numMines):
        self.size = size
        self.board = BoardGenerator(size, numMines).board
        self.fieldsRevealed = 0
        self.numMines = numMines
        self.gameOver = False
        self.victory = False

        self.network = BayesianNetwork(size=size, numMines=numMines)

    def reveal_field(self, x, y):
        def reveal_tile(x, y):
            revealed = []
            queue = [(x, y)]
            while len(queue) > 0:
                i, j = queue.pop()
                if not self.mine(i, j) and (i, j) not in revealed:
                    revealed.append((i, j))
                    if self.neighbours_with_mines(i, j) < 1:
                        queue.extend(neighbours(i, j, self.size))

            if (x, y) not in revealed:
                revealed.append((x, y))

            return revealed

        tile = self.board[x][y]
        revealed_tiles = reveal_tile(x, y)
        self.fieldsRevealed += len(revealed_tiles)

        for (i, j) in revealed_tiles:
            self.board[i][j].reveal()

        if tile.mine:
            self.gameOver = True
            self.victory = False
        else:
            fields_values = map(lambda (x, y): self.neighbours_with_mines(x,y), revealed_tiles)
            self.network.reveal_fields_without_mine(zip(revealed_tiles, fields_values))
            if self.fieldsRevealed + self.numMines >= self.size * self.size:
                self.gameOver = True
                self.victory = True

        return revealed_tiles

    def mine(self, x, y):
        return self.board[x][y].mine

    def neighbours_with_mines(self, x, y):
        return self.board[x][y].neighbours_with_mines

    def get_safe(self):
        return self.network.find_best_nodes()
