import tkinter as tk

from gui.main_dialog import MainDialog

if __name__ == '__main__':
    root = tk.Tk()
    dialog = MainDialog(root)
    root.protocol('WM_DELETE_WINDOW', dialog.on_close)
    root.mainloop()