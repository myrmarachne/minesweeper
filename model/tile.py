class Tile:
    def __init__(self, x_coord, y_coord):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.revealed = False

        # determines whether the tile contains a mine or not
        self.mine = False

        # the number of neighbouring fields containing mines
        self.neighbours_with_mines = 0

    def reveal(self):
        self.revealed = True

