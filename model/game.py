from bayesian_network import BayesianNetwork
from board_generator import BoardGenerator
from utils import str_join


class Game:
    def __init__(self, size=6, numMines=15):
        self.size = size
        self.board = BoardGenerator(size, numMines).board
        self.fieldsRevealed = 0
        self.numMines = numMines
        self.gameOver = False

        self.network = BayesianNetwork(size=size, numMines=numMines)

    def play(self):
        while not self.gameOver:
            self.print_board()
            self.print_safe()
            tile = self.prompt_for_field()
            self.reveal_field(tile)

    def reveal_field(self, tile):
        self.fieldsRevealed += 1
        tile.reveal()
        if tile.mine:
            self.gameOver = True
            print ("GAME OVER")
        else:
            self.network.reveal_field_without_mine(tile.x_coord, tile.y_coord, tile.neighbours_with_mines)

            if self.fieldsRevealed + self.numMines == self.size * self.size:
                self.gameOver = True
                print("You won")

    def print_safe(self):
        print("The most safe fields are: ")
        print(self.network.find_best_nodes())

    def print_board(self):
        for row in self.board:
            print map(lambda x: "[ ]" if not x.revealed else str_join('[', x.neighbours_with_mines, ']'), row)

    def prompt_for_field(self):
        user_input = raw_input("Provide the coordinates of the field you would like to use: ")

        # validate the user input
        try:
            x, y = map(lambda x: int(x), user_input.split(' ', 1))
            tile = self.board[x][y]

            # check if the field was already revealed
            if tile.revealed:
                return self.prompt_for_field()
            return tile

        except ValueError:
            print("The provided coordinates are not correct")
            return self.prompt_for_field()