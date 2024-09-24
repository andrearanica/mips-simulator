from libs.utils import int_to_bits
from libs.constants import REGISTERS_NAMES
from libs.instructions import get_instruction_object_from_binary
from libs.constants import opcodes, FUNCT_CODES

class Assembler:
    def __init__(self, instructions: list=[]) -> None:
        self.__instructions = instructions

    def get_assembled_program(self):
        """ Returns the list of instructions as binary strings
        """
        converted_instructions = []
        
        for instruction in self.__instructions:
            converted_instruction = self.__convert_instruction(instruction)
            converted_instructions.append(converted_instruction)

        return converted_instructions

    def __convert_instruction(self, instruction: str):
        """ Returns the instruction as an instance of instruction classes
        """
        first_word = instruction.split(' ')[0]
        
        opcode = opcodes.get(first_word)

        if opcode == None:
            raise RuntimeError(f'''Instruction {instruction} is not supported by 
                               the assembler; opcode is not defined''')
        
        if opcode == 0:
            # R-Type instruction -> opcode | rs | rt | rd | shamt | funct
            funct_code = FUNCT_CODES.get(first_word)
            if funct_code == None:
                raise RuntimeError(f'''Instruction {instruction} is not supported by 
                                   the assembler; funct code is not defined''')
            _, rd, rs, rt = instruction.replace(',', '').split(' ')
            
            shamt = 0x0
            if first_word == 'sll':
                shamt = int(rt)
            
            rd = [i for i, register in REGISTERS_NAMES.items() if register == rd][0]
            rs = [i for i, register in REGISTERS_NAMES.items() if register == rs][0]
            rt = [i for i, register in REGISTERS_NAMES.items() if register == rt][0]

            rd_str = int_to_bits(int(rd), 5)
            rs_str = int_to_bits(int(rs), 5)
            rt_str = int_to_bits(int(rt), 5)
            shamt_str = int_to_bits(int(shamt), 5)

            instruction_str = f'{int_to_bits(opcode, 6)}{rs_str}{rt_str}{rd_str}{shamt_str}{int_to_bits(funct_code, 5)}'
        else:
            raise RuntimeError(f'Instruction {instruction} is not supported by the assembler')

        return get_instruction_object_from_binary(instruction_str)