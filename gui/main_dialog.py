from libs import utils, exceptions, constants
from libs.datapath import Datapath
from libs.constants import REGISTERS_NAMES
from gui.terminal import Terminal

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox

class MainDialog:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title = 'MIPS Simulator'
        self.__build_dialog()
        self.datapath = Datapath()
        self.pointed_pc = None

    def __build_dialog(self):
        # Draw the dialog structure
        self.root.geometry('1000x500')
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

        # self.terminal_button = tk.Button(self.root, text='Open console', command=self.launch_console)
        # self.terminal_button.grid(row=2, column=5)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.place(x=350, y=75, width=625, height=300)
        self.code_textbox = tk.Text(self.notebook)
        self.memory_table = ttk.Treeview(self.notebook, columns=('', 'address', 'value'), show='headings')
        self.memory_table.heading('', text='')
        self.memory_table.heading('address', text='Address')
        self.memory_table.heading('value', text='Value')
        self.memory_table.column('', width=20, stretch=False)
        self.memory_table.column('address', width=100, stretch=False)
        self.memory_table.column('value', width=505, stretch=False)
        
        self.notebook.add(self.code_textbox, text='Code')
        self.notebook.add(self.memory_table, text='Memory')

        self.registers_table = ttk.Treeview(self.root, columns=('register', 'value'), show='headings')
        self.registers_table.place(x=25, y=75, width=300, height=300)
        self.registers_table.heading('register', text='Register')
        self.registers_table.heading('value', text='Value')
        self.registers_table.column('register', width=149)
        self.registers_table.column('value', width=149)

        self.message_label = tk.Label(self.root, text='')
        self.message_label.grid(row=70, column=2)

        self.run_button = tk.Button(self.root, text='Run', command=self.run_code)
        self.run_button.grid(row=75, column=1)
        self.step_by_step_button = tk.Button(self.root, text='Step by Step', command=self.run_code_step_by_step)
        self.step_by_step_button.grid(row=75, column=3)

        self.__reset_interface()

    def on_click_button_import_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r+') as file_reader:
                file_content = file_reader.read()
            if not utils.is_binary_program_valid(file_content):
                messagebox.askokcancel('Error', 'The imported file is not a valid file; please check that the syntax is correct')
            else:
                self.__reset_interface()
                self.instructions = utils.split_program_to_instructions(file_content)
                for i, instruction in enumerate(self.instructions):
                    self.code_textbox.insert(tk.END, f'{i} | {instruction}\n')
                self.datapath.load_program_in_memory(self.instructions)
                self.__update_interface()

    def on_click_button_reset(self):
        self.instructions = []
        self.datapath = Datapath()
        self.__reset_interface()

    def run_code(self):
        # FIXME crash if launching a program the second time
        self.datapath.run()
        self.message_label.config(text='Execution stopped')
        self.__update_interface()

    def run_code_step_by_step(self):
        self.pointed_pc = self.datapath.PC
        try:
            self.datapath.run_single_instruction()
        except exceptions.BreakException:
            self.message_label.config(text='Execution stopped using break instruction')

        self.__update_interface()
        # If BreakException write the end message
    
    def __reset_interface(self):
        # Reset register table
        for item in self.registers_table.get_children():
            self.registers_table.delete(item)
        for register_number in range(32):
            self.registers_table.insert('', tk.END, values=(REGISTERS_NAMES.get(register_number), 0))

        # Reset code textbox
        self.code_textbox.delete('1.0', tk.END)
        for item in self.memory_table.get_children():
            self.memory_table.delete(item)
        self.message_label.config(text='')

    def __update_interface(self):
        for item in self.registers_table.get_children():
            self.registers_table.delete(item)
        for register_number, register_value in enumerate(self.datapath.register_file.registers):
            self.registers_table.insert('', tk.END, values=(REGISTERS_NAMES.get(register_number), register_value))
        
        # I write a row for each word, so I group 4 bytes to write a row
        for item in self.memory_table.get_children():
            self.memory_table.delete(item)
        
        memory_row = ''
        word_address = 0
        for i, (address, value) in enumerate(self.datapath.memory.get_data().items()):    
            memory_row = utils.int_to_bits(value, 8) + memory_row
            if i+1 and (i+1) % 4 == 0:
                pos_char = ' '
                if self.datapath.PC == word_address:
                    pos_char = '*'
                self.memory_table.insert('', tk.END, values=(pos_char, word_address, memory_row))
                memory_row = ''
            if (i+1) % 4 == 1:
                word_address = address
    
    def launch_console(self):
        root = tk.Tk()
        terminal = Terminal(root)
        root.mainloop()