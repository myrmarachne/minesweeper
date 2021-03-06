from model.game import Game
from gui.main_window import MainWindow
import Tkinter as tk
import tkMessageBox
import sys


class Controller:
    def __init__(self):
        self.root = tk.Tk()

        self.size = tk.StringVar()
        self.num_mines = tk.StringVar()
        self.size.set(6)
        self.num_mines.set(3)

        self.model = Game(int(self.size.get()), int(self.num_mines.get()))
        self.view = MainWindow(self.root, self.model, self.reveal_field, self.reset_game, self.size, self.num_mines)

    def run(self):
        self.root.title("Minesweeper")
        self.root.deiconify()
        self.root.mainloop()

    def reset_game(self):
        try:
            self.model = Game(int(self.size.get()), int(self.num_mines.get()))
        except ValueError:
            self.model = Game()

        self.view.reset_view(self.model, self.reveal_field)

    def game_over(self):
        if self.model.victory:
            play_again = tkMessageBox.askyesno("Game over", "Congratulations, you won! Do you want to play again?")
            if play_again:
                self.reset_game()
            else:
                sys.exit()
        else:
            play_again = tkMessageBox.askyesno("Game over", "You're a loser! Do you want to play again?")
            if play_again:
                self.reset_game()
            else:
                sys.exit()

    def reveal_field(self, x_coord, y_coord):
        # Update the model
        revealed = self.model.reveal_field(x_coord, y_coord)

        # Update the view
        self.view.update_game_view(revealed)

        # Check if game is over
        if self.model.gameOver:
            self.game_over()
