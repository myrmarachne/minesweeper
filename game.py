from bayesian_network import BayesianNetwork
from board_generator import BoardGenerator
from utils import str_join

class Game:
    def __init__(self, size=3, numMines=2):
        self.size = size
        self.board = BoardGenerator(size, numMines)
        self.revealedBoard = [[False for i in range(0, size)] for j in range(0, size)]
        self.fieldsRevealed = 0
        self.numMines = numMines
        self.gameOver = False

        self.network = BayesianNetwork()
        self.network.read_from_file()

    def play(self):
        while not self.gameOver:
            self.print_board()
            self.print_safe()
            coordinates = self.prompt_for_field()
            self.reveal_field(coordinates)

    def reveal_field(self, coordinates):
        self.fieldsRevealed += 1
        self.revealedBoard[coordinates[0]][coordinates[1]] = True
        if self.board.board[coordinates[0]][coordinates[1]] == -1:
            self.gameOver = True
            print ("GAME OVER")
        else:
            self.network.reveal_field_without_mine(coordinates[0], coordinates[1],
                                                   self.board.board[coordinates[0]][coordinates[1]])

            if self.fieldsRevealed + self.numMines == self.size * self.size:
                self.gameOver = True
                print("You won")

    def print_safe(self):
        print("The most safe fields are: ")
        print(self.network.find_best_nodes())

    def print_board(self):
        board = map(lambda row: zip(row[0], row[1]), zip(self.revealedBoard, self.board.board))

        for row in board:
            print map(lambda (x, y): "[ ]" if x is False else str_join('[', y, ']'), row)

    def prompt_for_field(self):
        user_input = raw_input("Provide the coordinates of the field you would like to use: ")

        # validate the user input
        try:
            coordinates = map(lambda x: int(x), user_input.split(' ', 1))

            # check if the field was already revealed
            if self.revealedBoard[coordinates[0]][coordinates[1]]:
                return self.prompt_for_field()
            return coordinates

        except ValueError:
            print("The provided coordinates are not correct")
            return self.prompt_for_field()