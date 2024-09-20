from libs.instructions import get_instruction_object_from_binary
from libs.instructions import *
from libs.constants import opcodes

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
        instruction_obj = None

        first_word = instruction.split(' ')[0]

        instruction_obj = get_instruction_object_from_binary(instruction)
        
        return instruction_obj