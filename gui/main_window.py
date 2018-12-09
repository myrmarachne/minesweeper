import Tkinter as tk
from gui.game_frame import GameFrame
from gui.top_panel import TopPanel


class MainWindow:
    def __init__(self, window, model, click_event_handler, reset_event_hanler, size, num_mines, tile_size=48):
        self.window = window
        self.window.resizable(width=False, height=False)

        # Initialize the main
        self.top_panel = TopPanel(self.window, reset_event_hanler, size, num_mines)
        self.game_frame = GameFrame(self.window, model, click_event_handler, tile_size)

    def reset_view(self, model, event_handler):
        self.game_frame.reset(model, event_handler)

    def update_game_view(self, revealed_fields):
        self.game_frame.update_revealed_fields(revealed_fields)
        self.game_frame.match_safe()

