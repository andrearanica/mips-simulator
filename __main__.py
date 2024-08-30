import tkinter as tk

from gui.main_dialog import MainDialog
from libs.simulator import Simulator

if __name__ == '__main__':
    root = tk.Tk()
    dialog = MainDialog(root)
    root.mainloop()
