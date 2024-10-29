from libs.utils import *
from libs.constants import REGISTERS_NAMES, OPCODES, FUNCT_CODES, ITYPE_OPCODES, DATA_SEGMENT_START, TEXT_SEGMENT_START
from libs.instructions import get_instruction_object_from_binary

class Assembler:
    def __init__(self, instructions: list=[]) -> None:
        self.__data = []
        self.__text = []
        self.instructions = instructions
        self.__data_labels = {}
        self.__text_labels = {}

    @property
    def instructions(self) -> list:
        return self.__data.extend(self.__text)
    
    @instructions.setter
    def instructions(self, instructions: list):
        i = 0
        if not '.data' in instructions:
            self.__text = [instruction for instruction in instructions if not '.text' in instruction]
        else:
            is_data_segment = True

            for instruction in instructions:
                if is_data_segment:
                    if instruction == '.text':
                        is_data_segment = False
                    elif instruction != '.data':
                        self.__data.append(instruction)
                else:
                    self.__text.append(instruction)

    def get_assembled_program(self):
        """ Returns the list of instructions as binary strings
        """
        # self.__get_labels()
        
        converted_instructions = []

        for i, instruction in enumerate(self.__text):
            if not instruction:
                continue
            
            if ':' in instruction:
                _, instruction = instruction.split(':')
                instruction = instruction[1:]
                
            converted_instruction = self.__convert_instruction(instruction)
            converted_instructions.append(converted_instruction)

        return converted_instructions

    def __get_labels(self):
        for data in self.__data:
            if not data:
                continue
            label, directive_with_value = data.split(':')
            label = label.replace(' ', '')
            _, directive, value = directive_with_value.split(' ')
            # TODO check that directive is a regex
            directive = directive.replace(' ', '')

            if len(self.__data_labels.keys()):
                address = max([address for label, address in self.__data_labels.items()]) + 4
            else:
                address = DATA_SEGMENT_START

            self.__data_labels[label] = address

        for i, instruction in enumerate(self.__text):
            if not instruction:
                continue
                
            if ':' in instruction:
                label, _ = instruction.split(':')
                self.__text_labels[label] = TEXT_SEGMENT_START + 4*i

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
            
            if not is_number(immediate):
                raise RuntimeError('Labels are not supported yet')
                # immediate = self.__text_labels.get(immediate)
                # if immediate == None:
                #     raise RuntimeError(f'Label {immediate} has not been defined')

            opcode_str = int_to_bits(int(opcode), 6)
            immediate_str = int_to_bits(int(immediate), 26, True)

            instruction_str = f'{opcode_str}{immediate_str}'
        
        elif opcode == OPCODES.get('lw') or opcode == OPCODES.get('sw'):
            _, rt, offset_with_base = instruction.replace(',', '').split(' ')
            offset, base_register = offset_with_base.replace(')', '').split('(')
            
            if not is_number(offset):
                raise RuntimeError('Labels are not supported yet')
                # offset = self.__text_labels.get(immediate)
                # if offset == None:
                #     raise RuntimeError(f'Label {offset} has not been defined')
            
            opcode_str = int_to_bits(int(opcode), 6)
            rt = get_register_number_from_name(rt)
            base_register = get_register_number_from_name(base_register)
            rt_str = int_to_bits(rt, 5)
            base_register_str = int_to_bits(base_register, 5)
            offset_str = int_to_bits(int(offset), 16, True)

            instruction_str = f'{opcode_str}{base_register_str}{rt_str}{offset_str}'

        elif opcode in [o for _, o in ITYPE_OPCODES.items()]:
            _, rt, rs, immediate = instruction.replace(',', '').split(' ')
            
            if not is_number(immediate):
                raise RuntimeError('Labels are not supported yet')
                # immediate = self.__text_labels.get(immediate)
                # if immediate == None:
                #     raise RuntimeError(f'Label {immediate} has not been defined')

            rs = get_register_number_from_name(rs)
            rt = get_register_number_from_name(rt)
            
            opcode_str = int_to_bits(opcode, 6)
            rs_str = int_to_bits(rs, 5)
            rt_str = int_to_bits(rt, 5)
            immediate_str = int_to_bits(int(immediate), 16, True)
            
            instruction_str = f'{opcode_str}{rs_str}{rt_str}{immediate_str}'
        else:
            raise RuntimeError(f'Instruction {instruction} is not supported by the assembler')

        return get_instruction_object_from_binary(instruction_str)