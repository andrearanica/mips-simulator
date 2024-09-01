from libs import utils
from libs.simulator import Simulator
from libs.constants import REGISTERS_NAMES

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox

class MainDialog:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title = 'MIPS Simulator'
        self.__build_dialog()
        self.simulator = Simulator()

    def __build_dialog(self):
        # Draw the dialog structure
        self.root.geometry("1000x450")
        for i in range(5):
            self.root.columnconfigure(i, weight=1, minsize=50)
            
        for i in range(100):
            self.root.rowconfigure(i, minsize=5)

        self.root.resizable(width=False, height=False)

        # Add widgets
        self.title_label = tk.Label(self.root, text='MIPS simulator')
        self.title_label.grid(row=1, column=2)

        self.import_file_button = tk.Button(self.root, text='Open file', command=self.on_click_button_import_file)
        self.import_file_button.grid(row=2, column=1)

        self.reset_button = tk.Button(self.root, text='Reset', command=self.on_click_button_reset)
        self.reset_button.grid(row=2, column=3)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.place(x=350, y=75, width=625, height=300)
        self.code_textbox = tk.Text(self.notebook)
        self.memory_textbox = tk.Text(self.notebook)
        
        self.notebook.add(self.code_textbox, text='Code')
        self.notebook.add(self.memory_textbox, text='Memory')

        self.registers_table = ttk.Treeview(self.root, columns=('Register', 'Value'), show='headings')
        self.registers_table.place(x=25, y=75, width=300, height=300)
        self.registers_table.heading('Register', text='Register')
        self.registers_table.heading('Value', text='Value')
        self.registers_table.column('Register', width=149)
        self.registers_table.column('Value', width=149)
        self.__reset_interface()

        self.run_button = tk.Button(self.root, text='Run', command=self.run_code)
        self.run_button.grid(row=70, column=2)

    def on_click_button_import_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r+') as file_reader:
                file_content = file_reader.read()
            if not utils.is_binary_program_valid(file_content):
                messagebox.askokcancel('Error', 'The imported file is not a valid file; please check that the syntax is correct')
            else:
                self.__reset_interface()
                self.simulator.instructions = utils.split_program_to_instructions(file_content)
                for i, instruction in enumerate(self.simulator.instructions):
                    self.code_textbox.insert(tk.END, f'{i} | {instruction}\n')

    def on_click_button_reset(self):
        self.simulator.reset()
        self.__reset_interface()

    def run_code(self):
        self.simulator.run()
        self.__update_interface()
    
    def __reset_interface(self):
        # Reset register table
        for item in self.registers_table.get_children():
            self.registers_table.delete(item)
        for register_number in range(32):
            self.registers_table.insert('', tk.END, values=(REGISTERS_NAMES.get(register_number), 0))

        # Reset code textbox
        self.code_textbox.delete("1.0", tk.END)
        self.memory_textbox.delete("1.0", tk.END)

    def __update_interface(self):
        for item in self.registers_table.get_children():
            self.registers_table.delete(item)
        for register_number, register_value in enumerate(self.simulator.datapath.register_file.registers):
            self.registers_table.insert('', tk.END, values=(REGISTERS_NAMES.get(register_number), register_value))
        # I write a row for each word, so I group 4 bytes to write a row
        self.memory_textbox.delete("1.0", tk.END)
        memory_row = ''
        word_address = 0
        for i, (address, value) in enumerate(self.simulator.datapath.memory.get_data().items()):
            memory_row = utils.int_to_bits(value, 8) + memory_row
            if i+1 and (i+1) % 4 == 0:
                self.memory_textbox.insert(tk.END, f'{word_address} | {memory_row}\n')
                memory_row = ''
            if (i+1) % 4 == 1:
                word_address = address