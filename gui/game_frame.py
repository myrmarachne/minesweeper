import Tkinter as tk
from os.path import join, isfile
from os import getcwd, listdir

from gui.status_bar import StatusBar


class GameFrame:
    def __init__(self, root, model, event_handler, tile_size):
        self.model = model
        self.tile_size = tile_size
        self.safe_fields = []
        self.board_frame = None
        self.root = root

        # Initialize the images and the board
        self.images = self.initialize_images()
        self.board = self.initialize_board(event_handler)

        # Initialize the status bar
        self.status_bar = StatusBar(root, "")

    def reset(self, model, event_handler):
        # Reset the game frame view
        self.model = model
        self.board_frame.pack_forget()
        self.board = self.initialize_board(event_handler)
        self.safe_fields = []

    def initialize_images(self):
        path_to_images = join(getcwd(), "gui", "images")
        all_images = [f for f in listdir(path_to_images) if isfile(join(path_to_images, f)) and f.endswith("png")]
        images = {}

        def get_image_path(name):
            return join(path_to_images, filter(lambda f: f.startswith(name), all_images)[0])

        def resize_tile(img, tile_size):
            img = img.zoom(tile_size)
            img = img.subsample(img.width()/tile_size)
            return img

        for i in range(0, 9):
            try:
                img = tk.PhotoImage(file=get_image_path(str(i)))
                images[i] = resize_tile(img, self.tile_size)
            except KeyError:
                pass

        img = tk.PhotoImage(file=get_image_path("mine"))
        images["mine"] = resize_tile(img, self.tile_size)

        img = tk.PhotoImage(file=get_image_path("not_revealed"))
        images["not_revealed"] = resize_tile(img, self.tile_size)

        img = tk.PhotoImage(file=get_image_path("safe"))
        images["safe"] = resize_tile(img, self.tile_size)

        return images

    def initialize_board(self, event_handler):
        self.board_frame = tk.Frame(self.root, relief=tk.SUNKEN)
        size = self.model.size

        def init_tile(x_coord, y_coord, size=self.tile_size):
            frame = tk.Frame(self.board_frame, height=size, width=size)

            button = tk.Button(frame, state="normal", height=size, width=size, borderwidth=0)
            button["image"] = self.images["not_revealed"]
            button.pack(fill=tk.BOTH)
            button.bind("<Button-1>", lambda event, x=x_coord, y=y_coord: event_handler(x, y))
            button.bind("<Enter>", lambda event, model=self.model, x=x_coord, y=y_coord: self.status_bar.update(str(model.get_probability(x,y))))
            button.bind("<Leave>", lambda event: self.status_bar.clear())

            frame.pack_propagate(False)
            frame.grid(row=x_coord, column=y_coord)

            return button

        board = [[init_tile(x, y) for y in range(0, size)] for x in range(0, size)]
        self.board_frame.pack(padx=40, pady=10, side=tk.TOP)

        return board

    def update_revealed_fields(self, revealed_fields):

        for (x, y) in self.safe_fields:
            self.board[x][y]["image"] = self.images["not_revealed"]

        # Change the images shown on the revealed fields
        def disable_field(field, img):
            field["state"] = "disabled"
            field["image"] = img
            field["relief"] = tk.SUNKEN

        for (x, y) in revealed_fields:
            if self.model.mine(x,y):
                disable_field(self.board[x][y], self.images["mine"])
            else:
                neighbours_with_mines = self.model.neighbours_with_mines(x, y)
                disable_field(self.board[x][y], self.images[neighbours_with_mines])

    def match_safe(self):
        self.safe_fields = self.model.get_safe()

        for (x, y) in self.safe_fields:
            # Match the (x, y) field
            self.board[x][y]["image"] = self.images["safe"]

