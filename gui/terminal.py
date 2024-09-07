import tkinter as tk

class Terminal:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title = 'Terminal'
        self.__build_dialog()
    
    def __build_dialog(self):
        self.root.geometry('800x300')
        for i in range(2):
            self.root.rowconfigure(i, weight=1, minsize=150)
        # Transmitter is output, receiver is input
        self.transmitter_textbox = tk.Text(self.root, width=800)
        self.transmitter_textbox.grid(row=0, column=1)
        self.receiver_textbox = tk.Text(self.root, width=800)
        self.receiver_textbox.grid(row=1, column=1)