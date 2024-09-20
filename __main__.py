import tkinter as tk
from libs import assembler

from gui.main_dialog import MainDialog

if __name__ == '__main__':
    root = tk.Tk()
    dialog = MainDialog(root)
    # root.mainloop()
    instructions = [
        'addi $t0, $t0, 0x1'
    ]
    assembler = assembler.Assembler(instructions)
    assembled_program = assembler.get_assembled_program()
    for instruction in assembled_program:
        print(instruction)
