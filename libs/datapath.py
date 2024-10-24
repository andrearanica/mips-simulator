from enum import Enum

from libs.alu import ALU
from libs.alu_operations import AluOperations
from libs.memory import Memory
from libs.register_file import RegisterFile
from libs.instructions import *
from libs.constants import MEMORY_DIM, BREAK_INSTRUCTION, TEXT_SEGMENT_START, OPCODES, RTYPE_OPCODE
from libs.exceptions import *
from libs.utils import is_break_instruction, int_to_bits, bits_to_int, is_address_valid


class DatapathStates(Enum):
    OK = 'DATAPATH_OK'
    BREAK = 'DATAPATH_BREAK'
    MEMORY_ADDRESS_EXCEPTION = 'MEMORY_ADDRESS_NOT_VALID'
    INSTRUCTION_EXCEPTION = 'INSTRUCTION_NOT_VALID'


class Datapath:
    def __init__(self) -> None:
        self.__PC = TEXT_SEGMENT_START
        self.__A = 0
        self.__B = 0
        self.__alu = ALU()
        self.__memory = Memory()
        self.__register_file = RegisterFile()
        self.__alu_out = 0
        self.__state = DatapathStates.OK

    @property
    def memory(self) -> Memory:
        return self.__memory
    
    @property
    def register_file(self) -> RegisterFile:
        return self.__register_file
    
    @property
    def PC(self) -> int:
        return self.__PC
    
    @property
    def state(self) -> DatapathStates:
        return self.__state

    def run(self) -> None:
        while self.state != DatapathStates.BREAK:
            self.run_single_instruction()

    def run_single_instruction(self):
        self.__state = DatapathStates.OK
        try:
            self.__run_instruction()
        except Exception as e:
            self.__handle_exception(e)

    def __handle_exception(self, exception: Exception):
        if isinstance(exception, BreakException):
            self.__state = DatapathStates.BREAK
        elif isinstance(exception, NotValidMemoryAddressException):
            self.__state = DatapathStates.MEMORY_ADDRESS_EXCEPTION
        elif isinstance(exception, EmptyInstructionException):
            pass
        else:
            # TODO manage other exceptions
            print(exception)

    def __run_instruction(self):
        """ Executes the instruction that is stored inside the PC
        """
        self.__state = DatapathStates.OK
        fetched_instruction = self.__fetch_instruction()
        if isinstance(fetched_instruction, BreakInstruction):
            raise BreakException('Execution stopped using break instruction')
        self.__decode_instruction(fetched_instruction)
        self.__execute_instruction(fetched_instruction)

    def load_program_in_memory(self, instructions: list) -> None:
        """ Loads the instructions inside the memory, starting from the text segment address
            and using the little endian encoding (less significative byte is stored as first
            byte of the word)
        """
        address_to_write = TEXT_SEGMENT_START
        if not BREAK_INSTRUCTION in instructions:
            instructions.append(BREAK_INSTRUCTION)
        
        for instruction in instructions:
            # I store in an array the bytes that compose the instruction
            bytes = [
                instruction[24:32],  # The first byte is the less significative (little endian)
                instruction[16:24],
                instruction[8:16],
                instruction[0:8]
            ]
            
            for byte in bytes:
                self.__memory.write_data(bits_to_int(byte), address_to_write)
                address_to_write += 1

    def __fetch_instruction(self):
        """ Reads from the memory the instruction stored at the PC
        """
        address = self.__PC

        self.__PC += 4
        instruction = ''

        # I read from the memory the 4 bytes that make the instruction
        for _ in range(4):
            instruction_part = self.__memory.get_data(address)
            instruction = int_to_bits(instruction_part, 8) + instruction
            address += 1

        if not int(instruction):
            raise EmptyInstructionException()

        # After the instruction has been fetched, I get the opcode to understand the type of the instruction (R-Type, I-Type...)
        return get_instruction_object_from_binary(instruction)

    def __decode_instruction(self, instruction: Instruction):
        if hasattr(instruction, 'rs') and hasattr(instruction, 'rt'):
            rs = instruction.rs
            rt = instruction.rt
            self.__A = self.__register_file.get_register(rs)
            self.__B = self.__register_file.get_register(rt)

        # I calculate the branch address, so if the instruction is a BEQ I already have it
        offset = str(instruction)[16:32]
        self.__alu.src_a = self.__PC-4
        print(self.__alu.src_a)
        self.__alu.src_b = bits_to_int(offset, True)
        
        self.__alu.alu_operation = AluOperations.SUM
        self.__alu_out = self.__alu.get_result()

    def __execute_instruction(self, instruction: Instruction):
        """ Executes the instruction depending on its type
        """
        if isinstance(instruction, RTypeInstruction):
            self.__execute_rtype_instruction(instruction)
        elif isinstance(instruction, ITypeInstruction):
            self.__execute_itype_instruction(instruction)
        elif isinstance(instruction, BranchOnEqualInstruction):
            self.__execute_beq_instruction(instruction)
        elif isinstance(instruction, JumpInstruction):
            self.__execute_jump_instruction(instruction)
        elif isinstance(instruction, SystemCallInstruction):
            pass
        else:
            raise NotValidInstructionException("Error trying to execute a not valid instruction")
    
    def __execute_rtype_instruction(self, instruction: RTypeInstruction):
        # The R-Type instructions use the two temp registers as ALU inputs
        self.__alu.src_a = self.__A
        self.__alu.src_b = self.__B
        
        # I need to get the funct code to understand which operation do
        if instruction.funct == 0x20:
            self.__alu.alu_operation = AluOperations.SUM
        elif instruction.funct == 0x22:
            self.__alu.alu_operation = AluOperations.SUB
        elif instruction.funct == 0x24:
            self.__alu.alu_operation = AluOperations.AND
        elif instruction.funct == 0x25:
            self.__alu.alu_operation = AluOperations.OR
        elif instruction.funct == 0x2a:
            self.__alu.alu_operation = AluOperations.SLT
        else:
            raise NotValidInstructionException(f'Instruction {instruction} not implemented')

        # I store the result of the operation inside the register
        result = self.__alu.get_result()
        self.__register_file.write(result, instruction.rd)

    def __execute_itype_instruction(self, instruction: ITypeInstruction):
        is_memory_instruction = False
        self.__alu.src_a = self.__A
        immediate = bits_to_int(str(instruction)[16:32], True)
        
        self.__alu.src_b = immediate

        # I understand the type of the instruction by the opcode
        if instruction.opcode == 0x8:
            self.__alu.alu_operation = AluOperations.SUM
        elif instruction.opcode == 0xc:
            self.__alu.alu_operation = AluOperations.AND
        elif instruction.opcode == 0xd:
            self.__alu.alu_operation = AluOperations.OR
        elif instruction.opcode == 0x23 or instruction.opcode == 0x2b:
            self.__alu.alu_operation = AluOperations.SUM
            is_memory_instruction = True
        elif instruction.opcode == 0xf:
            self.__alu.shamt = 16
            self.__alu.alu_operation = AluOperations.SLL
        else:
            raise NotValidInstructionException(f'Instruction {instruction} not implemented')

        result = self.__alu.get_result()
        if not is_memory_instruction:
            self.__register_file.write(result, instruction.rt)
        else:
            # If it is a memory instruction, the result is the address of the memory
            self.__execute_memory_instruction(instruction, result)

    def __execute_memory_instruction(self, instruction: ITypeInstruction, address: int):
        """ Writes or loads information from the memory
        """
        if not is_address_valid(address):
            raise NotValidMemoryAddressException(f'Address {address} is not aligned to the word')
        
        if instruction.opcode == 0x23:
            # Load word
            memory_data = self.memory.get_data(address)
            self.register_file.write(memory_data, instruction.rt)
        else:
            # Store word
            data_to_write = self.register_file.get_register(instruction.rt)
            data_to_write_str = str(int_to_bits(data_to_write, 32, True))
            print(data_to_write, data_to_write_str)

            bytes = [
                bits_to_int(data_to_write_str[24:32]),
                bits_to_int(data_to_write_str[16:24]),
                bits_to_int(data_to_write_str[8:16]),
                bits_to_int(data_to_write_str[0:8])
            ]

            for i in range(4):
                self.memory.write_data(bytes[i], address)
                address += 1
    
    def __execute_beq_instruction(self, instruction: BranchOnEqualInstruction):
        self.__alu.src_a = self.__A
        self.__alu.src_b = self.__B

        are_registers_equal = self.__alu.zero
        
        if are_registers_equal:
            new_address = self.__alu_out
            self.__PC = new_address
    
    def __execute_jump_instruction(self, instruction: JumpInstruction):
        # The new PC is formed by the last 26 bits of the instruction
        # shifted left and the 4 upper bits of the current PC
        address_str = int_to_bits(self.__PC)[0:4] + str(instruction.target) + '00'
        self.__PC = bits_to_int(address_str, True)