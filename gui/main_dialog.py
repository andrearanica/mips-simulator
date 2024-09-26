import os, json

from libs import utils, exceptions, constants
from libs.instructions import get_instruction_object_from_binary
from libs.assembler import Assembler
from libs.utils import convert
from libs.constants import Systems
from libs.datapath import Datapath, DatapathStates
from libs.constants import REGISTERS_NAMES, Languages
from libs.message_manager import MessageManager
from gui.terminal import Terminal

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox

class MainDialog:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title = 'MIPS Simulator'
        self.datapath = Datapath()
        self.config = self.__get_config()
        self.message_manager = MessageManager(self.config['language'])
        self.__build_dialog()

    def __get_config(self) -> dict:
        if not os.path.exists(constants.CONFIG_FILE_PATH):
            return constants.STANDARD_CONFIG
        with open(constants.CONFIG_FILE_PATH, 'r+') as file_reader:
            try:
                return json.loads(file_reader.read())
            except:
                return constants.STANDARD_CONFIG

    def set_system(self, system: int) -> None:
        self.config['system'] = system
        self.__update_interface()

    def set_language(self, language: str) -> None:
        self.config['language'] = language
        self.message_manager.language = language
        self.__update_interface()
        self.__reload_messages()

    def __build_dialog(self):
        # Draw the dialog structure
        self.root.geometry('1000x500')
        for i in range(5):
            self.root.columnconfigure(i, weight=1, minsize=50)
            
        for i in range(100):
            self.root.rowconfigure(i, minsize=5)

        self.root.resizable(width=False, height=False)

        # Add widgets
        self.__build_menu()

        self.title_label = tk.Label(self.root, text='MIPS simulator')
        self.title_label.grid(row=1, column=2)

        self.import_file_button = tk.Button(self.root, text=self.message_manager.get_message('OPEN_FILE'), command=self.on_click_button_import_file)
        self.import_file_button.grid(row=2, column=1)

        self.reset_button = tk.Button(self.root, text='Reset', command=self.on_click_button_reset)
        self.reset_button.grid(row=2, column=3)

        # self.terminal_button = tk.Button(self.root, text='Open console', command=self.launch_console)
        # self.terminal_button.grid(row=2, column=5)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.place(x=350, y=75, width=625, height=300)
        # self.code_textbox = tk.Text(self.notebook)
        self.memory_table = ttk.Treeview(self.notebook, columns=('', 'address', 'value'), show='headings')
        self.memory_table.heading('', text='')
        self.memory_table.heading('address', text='Address')
        self.memory_table.heading('value', text='Value')
        self.memory_table.column('', width=20, stretch=False)
        self.memory_table.column('address', width=100, stretch=False)
        self.memory_table.column('value', width=505, stretch=False)
        
        # self.notebook.add(self.code_textbox, text='Code')
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
        self.__reload_messages()    # FIXME why we need to call this function?

    def __build_menu(self):
        """ Builds the upper menu
        """
        self.menu_bar = tk.Menu(self.root)
        self.system_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.language_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=self.message_manager.get_message('SYSTEM'), menu=self.system_menu)
        self.menu_bar.add_cascade(label=self.message_manager.get_message('LANGUAGE'), menu=self.language_menu)

        label = self.message_manager.get_message('BINARY')
        if self.config['system'] == constants.Systems.BINARY.value:
            label += ' (*)'
        self.system_menu.add_command(label=label, command= lambda: self.set_system(constants.Systems.BINARY.value))
        
        label = self.message_manager.get_message('DECIMAL')
        if self.config['system'] == constants.Systems.DECIMAL.value:
            label += ' (*)'
        self.system_menu.add_command(label=label, command= lambda: self.set_system(constants.Systems.DECIMAL.value))
        
        label = self.message_manager.get_message('HEXADECIMAL')
        if self.config['system'] == constants.Systems.HEX.value:
            label += ' (*)'
        self.system_menu.add_command(label=label, command= lambda: self.set_system(constants.Systems.HEX.value))

        label = Languages.ITA.value.upper()
        if self.config['language'] == Languages.ITA.value:
            label += ' (*)'
        self.language_menu.add_command(label=label, command= lambda: self.set_language(Languages.ITA.value))
        
        label = Languages.ENG.value.upper()
        if self.config['language'] == Languages.ENG.value:
            label += ' (*)'
        self.language_menu.add_command(label=label, command= lambda: self.set_language(Languages.ENG.value))

        self.root.config(menu=self.menu_bar)

    def __reload_messages(self):
        """ Refreshes the text of the widgets that contain messages
        """
        self.import_file_button.config(text=self.message_manager.get_message('OPEN_FILE'))
        self.reset_button.config(text=self.message_manager.get_message('RESET'))
        self.run_button.config(text=self.message_manager.get_message('RUN'))
        self.step_by_step_button.config(text=self.message_manager.get_message('STEP_BY_STEP'))
        self.notebook.tab(0, text=self.message_manager.get_message('MEMORY'))
        # self.notebook.tab(1, text=self.message_manager.get_message('MEMORY'))
        self.registers_table.heading('register', text=self.message_manager.get_message('REGISTER'))
        self.registers_table.heading('value', text=self.message_manager.get_message('VALUE'))
        self.memory_table.heading('address', text=self.message_manager.get_message('ADDRESS'))
        self.memory_table.heading('value', text=self.message_manager.get_message('VALUE'))

    def on_click_button_import_file(self):
        file_path = filedialog.askopenfilename()
        self.instructions = []
        if file_path:
            with open(file_path, 'r+') as file_reader:
                file_content = file_reader.read()
                
            self.__reset_interface()
            if '.asm' in file_path:
                self.instructions = self.__get_assembled_program(file_content)
            else:
                if not utils.is_binary_program_valid(file_content):
                    messagebox.askokcancel('Error', 'The imported file is not a valid file; please check that the syntax is correct')
                else:
                    self.instructions = utils.split_program_to_instructions(file_content)
            # for i, instruction in enumerate(self.instructions):
                # self.code_textbox.insert(tk.END, f'{i} | {instruction}\n')
            self.datapath.load_program_in_memory([str(instruction) for instruction in self.instructions])
            self.__update_interface()

    def on_click_button_reset(self):
        self.instructions = []
        self.datapath = Datapath()
        self.__reset_interface()

    def run_code(self):
        self.datapath.run()
        self.message_label.config(text='Execution stopped')
        self.__update_interface()

    def run_code_step_by_step(self):
        text_segment_addresses = [address 
            for address in self.datapath.memory.get_data().keys() 
            if constants.TEXT_SEGMENT_START <= address < constants.DATA_SEGMENT_START]
        if self.datapath.PC <= max(text_segment_addresses):
            self.datapath.run_single_instruction()
        
        self.__update_interface()
    
    def __get_assembled_program(self, program: str):
        """ Gets the program file content and returns a list of instructions instances
        """
        instructions = program.split('\n')
        assembler = Assembler(instructions)
        return assembler.get_assembled_program()

    def __reset_interface(self):
        # Reset register table
        for item in self.registers_table.get_children():
            self.registers_table.delete(item)
        for register_number in range(32):
            self.registers_table.insert('', tk.END, values=(REGISTERS_NAMES.get(register_number), 0))

        # Reset code textbox
        # self.code_textbox.delete('1.0', tk.END)
        for item in self.memory_table.get_children():
            self.memory_table.delete(item)
        self.message_label.config(text='')

        self.__build_menu()

    def __update_interface(self):
        for item in self.registers_table.get_children():
            self.registers_table.delete(item)
        for register_number, register_value in enumerate(self.datapath.register_file.registers):
            self.registers_table.insert('', tk.END, values=(REGISTERS_NAMES.get(register_number), convert(register_value, self.config['system'])))
        
        for item in self.memory_table.get_children():
            self.memory_table.delete(item)
        
        memory_row = ''
        word_address = 0
        for i, (address, value) in enumerate(self.datapath.memory.get_data().items()):
            memory_row = utils.int_to_bits(value, 8) + memory_row
            # I write a row for each word, so I group 4 bytes to write a row
            if i+1 and (i+1) % 4 == 0:
                pos_char = ' '
                if self.datapath.PC == word_address:
                    pos_char = '*'
                memory_row_int = utils.bits_to_int(memory_row)
                
                if self.config['system'] == Systems.BINARY:
                    n_ciphers = 32
                else:
                    n_ciphers = None

                # I try to convert the row as an instruction
                memory_row_bits = utils.int_to_bits(memory_row_int, 32)
                try:
                    instruction = get_instruction_object_from_binary(memory_row_bits)
                except:
                    instruction = None
                
                if instruction != None:
                    # If it can be converted in an instruction, I display the instruction
                    self.memory_table.insert('', tk.END, values=(pos_char, convert(word_address, self.config['system'], n_ciphers), instruction.to_text()))
                else:
                    self.memory_table.insert('', tk.END, values=(pos_char, convert(word_address, self.config['system'], n_ciphers), convert(memory_row_int, self.config['system'], n_ciphers)))
                memory_row = ''
            if (i+1) % 4 == 1:
                word_address = address

        if self.datapath.state != DatapathStates.OK:
            self.message_label.config(text=self.message_manager.get_message(self.datapath.state.value))

        self.__build_menu()

    def launch_console(self):
        root = tk.Tk()
        root.mainloop()

    def launch_settings(self):
        pass

    def on_close(self):
        with open(constants.CONFIG_FILE_PATH, 'w+') as file_writer:
            file_writer.write(json.dumps(self.config))
        self.root.destroy()