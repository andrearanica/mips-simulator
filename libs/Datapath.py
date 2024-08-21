from ALU import ALU
from Memory import Memory
from RegisterFile import RegisterFile
from Instructions import Instruction, RTypeInstruction, ITypeInstruction, SystemCallInstruction, BranchOnEqualInstruction, JumpInstruction
from constants import MEMORY_DIM, BREAK_INSTRUCTION, TEXT_SEGMENT_START
from utils import is_break_instruction

class Datapath:
    def __init__(self) -> None:
        self.__PC = 0
        self.__A = 0
        self.__B = 0
        self.__alu = ALU()
        self.__memory = Memory(MEMORY_DIM)
        self.__register_file = RegisterFile()

    
    def run(self, instructions: list) -> None:
        """ Executes the passed instructions
        """
        last_instruction = instructions[::-1]
        if not is_break_instruction(last_instruction):
            instructions.append(BREAK_INSTRUCTION)
        
        self.__load_program_in_memory()

        can_continue = True
        i = 0
        while can_continue:
            try:
                instruction = self.__fetch_instruction()
                print(f"I fetched {instruction}")
            except:
                pass
            i += 1


    def __load_program_in_memory(self, instructions: list) -> None:
        """ Loads the instructions inside the memory, starting from the text segment address
            and using the little endian encoding (less significative byte is stored as first
            byte of the word)
        """
        address_to_write = TEXT_SEGMENT_START
        for instruction in instructions:
            # I store in an array the bytes that compose the instruction
            bytes = [
                instruction[(24, 32)],  # The first byte is the less significative (little endian)
                instruction[(16, 24)],
                instruction[(8, 16)],
                instruction[(0, 8)]
            ]
            
            for byte in bytes:
                self._memory.write_data(byte, address_to_write)
                address_to_write += 1
    
    def __fetch_instruction(self):
        """ Reads from the memory the instruction stored at the PC
        """
        address = self.__PC
        self.__PC += 4
        instruction = ''

        # I read from the memory the 4 bytes that make the instruction
        for i in range(4):
            instruction_part = self.__memory.get_data(address)
            instruction = instruction_part + instruction
            address += 1
        
        # After the instruction has been fetched, I get the opcode to understand the type of the instruction (R-Type, I-Type...)
        return self.__get_instruction_object(instruction)
    
    def __get_instruction_object(self, instruction: str):
        opcode = instruction[(0, 6)]
        funct = instruction[(26, 32)]

        if opcode == '000000':
            # It is an R-Type instruction
            if funct == '001100':
                instruction_obj = SystemCallInstruction()
            elif funct == '001101':                 # It is a break instruction
                raise RuntimeError('Execution stopped using break instruction')
            else:
                rs = int(instruction[(6, 11)])
                rt = int(instruction[(11, 16)])
                rd = int(instruction[(16, 21)])
                shamt = int(instruction[(21, 26)])
                funct = int(instruction[(26, 32)])
                instruction_obj = RTypeInstruction(int(opcode), rs, rt, rd, shamt, funct)
        elif opcode == '000100':
            # It is a BEQ instruction
            rs = int(instruction[(6, 11)])
            rt = int(instruction[(11, 16)])
            offset = int(instruction[(16, 32)])
            instruction_obj = BranchOnEqualInstruction(int(opcode), rs, rt, offset)
        elif opcode == '000010':
            # It is a jump instruction
            target = int(instruction[(6, 32)])
            instruction_obj = JumpInstruction(target)
        else:
            rs = int(instruction[(6, 11)])
            rt = int(instruction[(11, 16)])
            immediate = instruction[(16, 32)]
            instruction_obj = ITypeInstruction(int(opcode), rs, rt, immediate)

        return instruction_obj