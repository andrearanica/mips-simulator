import tkinter as tk
from libs import assembler

from gui.main_dialog import MainDialog

if __name__ == '__main__':
    root = tk.Tk()
    dialog = MainDialog(root)
    root.mainloop()
    # instructions = [
    #     'lw $t0, 4($t1)'
    # ]
    # assembler = assembler.Assembler(instructions)
    # assembled_program = assembler.get_assembled_program()
    # for instruction in assembled_program:
    #     print(instruction)
