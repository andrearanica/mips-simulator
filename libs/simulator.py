import os

from libs import utils, constants
from libs.datapath import Datapath

class Simulator:
    def __init__(self) -> None:
        self.__file_path = None
        self.__instructions = []
        self.__datapath = Datapath()

    @property
    def file_path(self) -> str:
        return self.__file_path
    
    @file_path.setter
    def file_path(self, file_path: str) -> None:
        if os.path.exists(file_path) or not file_path:
            self.__file_path = file_path
            if file_path:
                with open(self.__file_path, 'r+') as file_reader:
                    file_content = file_reader.read()
                    self.instructions = [row.strip() for row in file_content.split('\n')]
        else:
            raise RuntimeError(f'File {file_path} doesn\'t exist')
    
    @property
    def instructions(self) -> list:
        return self.__instructions
    
    @instructions.setter
    def instructions(self, instructions: list) -> None:
        for instruction in instructions:
            if not utils.is_valid_instruction(instruction):
                raise RuntimeError(f'Instruction {instruction} is not a valid instruction')
        last_instruction = instructions[::-1]
        if not utils.is_break_instruction(last_instruction):
            instructions.append(constants.BREAK_INSTRUCTION)
        self.__instructions = instructions
    
    @property
    def datapath(self) -> Datapath:
        return self.__datapath

    def run(self):
        if self.instructions:
            self.datapath.run(self.instructions)        

    def reset(self):
        self.file_path = ''
        self.instructions = []
        self.__datapath = Datapath()