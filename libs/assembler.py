from libs.utils import int_to_bits, get_register_number_from_name
from libs.constants import REGISTERS_NAMES, OPCODES, FUNCT_CODES, ITYPE_OPCODES
from libs.instructions import get_instruction_object_from_binary

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
        
        opcode = OPCODES.get(first_word)
        
        if opcode == None:
            raise RuntimeError(f'''Instruction {instruction} is not supported by 
                               the assembler; opcode is not defined''')
        
        if opcode == 0:
            # R-Type instruction -> opcode | rs | rt | rd | shamt | funct
            funct_code = FUNCT_CODES.get(first_word)
            if funct_code == None:
                raise RuntimeError(f'''Instruction {instruction} is not supported by 
                                   the assembler; funct code is not defined''')
            
            if first_word != 'sll':
                _, rd, rs, rt = instruction.replace(',', '').split(' ')
                shamt = 0
            else:
                _, rd, rt, shamt = instruction.replace(',', '').split(' ')
                rs = 0

            rd = [i for i, register in REGISTERS_NAMES.items() if register == rd][0]
            if first_word != 'sll':
                rs = [i for i, register in REGISTERS_NAMES.items() if register == rs][0]
            rt = [i for i, register in REGISTERS_NAMES.items() if register == rt][0]

            opcode_str = int_to_bits(opcode, 6)
            rd_str = int_to_bits(int(rd), 5)
            rs_str = int_to_bits(int(rs), 5)
            rt_str = int_to_bits(int(rt), 5)
            
            if first_word == 'sll':
                rs_str = int_to_bits(0, 5)

            shamt_str = int_to_bits(int(shamt), 5)

            instruction_str = f'{opcode_str}{rs_str}{rt_str}{rd_str}{shamt_str}{int_to_bits(funct_code, 6)}'
        
        elif opcode == OPCODES.get('j') or opcode == OPCODES.get('jal'):
            _, immediate = instruction.replace(',', '').split(' ')
            opcode_str = int_to_bits(int(opcode), 6)
            immediate_str = int_to_bits(int(immediate), 26)

            instruction_str = f'{opcode_str}{immediate_str}'
        
        elif opcode == OPCODES.get('lw') or opcode == OPCODES.get('sw'):
            _, rt, offset_with_base = instruction.replace(',', '').split(' ')
            offset, base_register = offset_with_base.replace(')', '').split('(')
            
            opcode_str = int_to_bits(int(opcode), 6)
            rt = get_register_number_from_name(rt)
            base_register = get_register_number_from_name(base_register)
            rt_str = int_to_bits(rt, 5)
            base_register_str = int_to_bits(base_register, 5)
            offset_str = int_to_bits(int(offset), 16)

            instruction_str = f'{opcode_str}{base_register_str}{rt_str}{offset_str}'

        elif opcode in [o for _, o in ITYPE_OPCODES.items()]:
            _, rt, rs, immediate = instruction.replace(',', '').split(' ')

            rs = get_register_number_from_name(rs)
            rt = get_register_number_from_name(rt)
            
            opcode_str = int_to_bits(opcode, 6)
            rs_str = int_to_bits(rs, 5)
            rt_str = int_to_bits(rt, 5)
            immediate_str = int_to_bits(int(immediate), 16)

            instruction_str = f'{opcode_str}{rs_str}{rt_str}{immediate_str}'
        else:
            raise RuntimeError(f'Instruction {instruction} is not supported by the assembler')

        return get_instruction_object_from_binary(instruction_str)