import Tkinter as tk


class StatusBar:
    def __init__(self, root, label):
        self.label = tk.StringVar()
        self.label.set(label)
        self.root = root
        self.initialize()

    def initialize(self):
        frame = tk.Frame(self.root, relief=tk.SUNKEN)
        label = tk.Label(frame, font=('arial', 12, 'normal'), textvariable=self.label, padx=10, pady=10)
        label.pack(fill=tk.X)
        frame.pack(side=tk.BOTTOM)

    def update(self, label):
        percent = int(float(label)*100)
        self.label.set("No mine probability: " + str(percent) + "%")

    def clear(self):
        self.label.set("")
