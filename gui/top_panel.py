import Tkinter as tk


class TopPanel:
    def __init__(self, root, reset_event_handler, size, numMines):
        self.root = root
        self.mines_number_field = None
        self.size_field = None
        self.reset_button = None
        self.initialize_frame(reset_event_handler, size, numMines)

    def initialize_frame(self, reset_event_handler, size, numMines):
        frame = tk.Frame(self.root, relief=tk.SUNKEN)

        tk.Label(frame, text="Size:", font=('arial', 12, 'normal')).grid(row=0, column=0, padx=10)
        self.size_field = tk.Entry(frame, font=('arial', 15, 'normal'), width=5, textvariable=size)
        self.size_field.grid(row=0, column=1, padx=10)

        tk.Label(frame, text="Mines:", font=('arial', 12, 'normal')).grid(row=0, column=2, padx=10)
        self.mines_number_field = tk.Entry(frame, font=('arial', 15, 'normal'), width=5, textvariable=numMines)
        self.mines_number_field.grid(row=0, column=3, padx=10)

        self.reset_button = tk.Button(frame, state="normal", text="New game")
        self.reset_button.grid(row=0, column=4, padx=10)

        self.reset_button.bind("<Button-1>", lambda event: reset_event_handler())

        frame.pack(padx=40, pady=40, side=tk.TOP, fill=tk.BOTH)
