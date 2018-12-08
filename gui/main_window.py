import Tkinter as tk
from os.path import join, isfile
from os import getcwd, listdir


class MainWindow:
    def __init__(self, window, model, event_handler, tile_size=40):
        self.window = window
        self.window.resizable(width=False, height=False)
        self.model = model
        self.tile_size = tile_size

        self.images = self.initialize_images()

        self.initialize_top_panel()
        self.status_bar_label = ""
        self.initialize_status_bar()

        self.board_frame = None
        self.board = self.initialize_board(model, event_handler)

        self.safe_fields = []

    def reset_view(self, model, event_handler):
        self.model = model
        self.board_frame.pack_forget()
        self.board = self.initialize_board(model, event_handler)
        self.safe_fields = []

    def initialize_top_panel(self):
        pass

    def initialize_status_bar(self):
        frame = tk.Frame(self.window, relief=tk.SUNKEN)
        label = tk.Label(frame, font=('arial', 12, 'normal'), text=self.status_bar_label)
        label.pack(fill=tk.X)
        frame.pack(side=tk.BOTTOM)

    def initialize_images(self):
        path_to_images = join(getcwd(), "gui", "images")
        all_images = [f for f in listdir(path_to_images) if isfile(join(path_to_images, f)) and f.endswith("png")]
        images = {}

        def get_image_path(name):
            return join(path_to_images, filter(lambda f: f.startswith(name), all_images)[0])

        def resize_tile(img, tile_size):
            return img.subsample(img.width() / tile_size)

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

    def initialize_board(self, model, event_handler):
        self.board_frame = tk.Frame(self.window, relief=tk.SUNKEN)
        size = model.size

        def init_tile(x_coord, y_coord, size=self.tile_size):
            frame = tk.Frame(self.board_frame, height=size, width=size)

            button = tk.Button(frame, state="normal", height=size, width=size)
            button["image"] = self.images["not_revealed"]
            button.pack(fill=tk.BOTH)
            button.bind("<Button-1>", lambda event, x=x_coord, y=y_coord: event_handler(x, y))

            frame.pack_propagate(False)
            frame.grid(row=x_coord, column=y_coord)

            return button

        board = [[init_tile(x, y) for y in range(0, size)] for x in range(0, size)]
        self.board_frame.pack(padx=10, pady=10, side=tk.TOP)

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
        safe_fields = self.model.get_safe()

        for (x, y) in safe_fields:
            # Match the (x, y) field
            self.board[x][y]["image"] = self.images["safe"]

        self.safe_fields = safe_fields
