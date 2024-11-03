import tkinter as tk
from libs.message_manager import MessageManager
from libs.datapath import Datapath, Console
from libs import constants

class ConsoleDialog:
    def __init__(self, root: tk.Tk, console: Console, main_dialog) -> None:
        self.root = root
        self.root.title('Console')
        self.console = console
        self.main_dialog = main_dialog
        self.__build_dialog()
    
    def __build_dialog(self):
        self.root.geometry('600x350')
        self.textbox = tk.Text(self.root)
        self.textbox.pack()
        self.textbox.bind('<KeyRelease>', self.on_write_char)
        self.refresh()

    def refresh(self):
        self.textbox.delete('1.0', tk.END)
        text = ''
        for data in self.console.data:
            text += chr(data)
        self.textbox.insert(tk.END, text)
    
    def on_write_char(self, event):
        if textbox_content := self.textbox.get("1.0", tk.END).replace('\n', ''):
            written_char = textbox_content[-1]
            self.console.set_received_data(ord(written_char))
            self.textbox.delete('1.0', tk.END)
            self.textbox.insert(tk.END, self.console.data)
            self.main_dialog.update_interface()