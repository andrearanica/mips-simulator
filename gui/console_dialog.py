import tkinter as tk
from libs.message_manager import MessageManager
from libs.datapath import Datapath
from libs.constants import *

class ConsoleDialog:
    def __init__(self, root: tk.Tk, console) -> None:
        self.root = root
        self.root.title('Console')
        self.console = console
        self.__build_dialog()
    
    def __build_dialog(self):
        self.root.geometry('600x350')
        self.textbox = tk.Text(self.root)
        self.textbox.pack()

    def refresh(self):
        self.textbox.delete('1.0', tk.END)
        text = ''
        for data in self.console.data:
            text += chr(data)
        self.textbox.insert(tk.END, text)