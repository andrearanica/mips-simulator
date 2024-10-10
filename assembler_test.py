from libs.assembler import Assembler

instructions = [
    '.data',
    'nome: .word 16'
    '.text',
    'addi $t0, $t0, 1',
    'j palle',
    'addi $t1, $t1, 2',
    'palle: addi $t0, $t0, 1',
    'beq $t0, $t0, palle'
]

assembler = Assembler(instructions)
assembled_program = assembler.get_assembled_program()

for instruction in assembled_program:
    print(instruction.to_text())