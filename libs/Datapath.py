from .ALU import ALU
from .AluOperations import AluOperations
from .Memory import Memory
from .RegisterFile import RegisterFile
from .Instructions import Instruction, RTypeInstruction, ITypeInstruction, SystemCallInstruction, BranchOnEqualInstruction, JumpInstruction
from .constants import MEMORY_DIM, BREAK_INSTRUCTION, TEXT_SEGMENT_START
from .exceptions import NotValidInstructionException, BreakException
from .utils import is_break_instruction, int_to_bits, bits_to_int, is_address_valid

class Datapath:
    def __init__(self) -> None:
        self.__PC = TEXT_SEGMENT_START
        self.__A = 0
        self.__B = 0
        self.__alu = ALU()
        self.__alu_out = 0
        self.__memory = Memory(MEMORY_DIM)
        self.__register_file = RegisterFile()

    @property
    def memory(self) -> Memory:
        return self.__memory
    
    @property
    def register_file(self) -> RegisterFile:
        return self.__register_file
    
    def run(self, instructions: list) -> None:
        """ Executes the passed instructions
        """
        last_instruction = instructions[::-1]
        if not is_break_instruction(last_instruction):
            instructions.append(BREAK_INSTRUCTION)
        
        self.__load_program_in_memory(instructions)

        can_continue = True
        i = 0
        while can_continue:
            try:
                fetched_instruction = self.__fetch_instruction()
                self.__decode_instruction(fetched_instruction)
                self.__execute_instruction(fetched_instruction)
                i += 1
            except BreakException:
                # FIXME add exception handler
                can_continue = False
        
        # print(self.__register_file)

    def __load_program_in_memory(self, instructions: list) -> None:
        """ Loads the instructions inside the memory, starting from the text segment address
            and using the little endian encoding (less significative byte is stored as first
            byte of the word)
        """
        address_to_write = TEXT_SEGMENT_START
        for instruction in instructions:
            # I store in an array the bytes that compose the instruction
            bytes = [
                instruction[24:32],  # The first byte is the less significative (little endian)
                instruction[16:24],
                instruction[8:16],
                instruction[0:8]
            ]
            
            for byte in bytes:
                # TODO
                self.__memory.write_data(bits_to_int(byte), address_to_write)
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
            instruction = int_to_bits(instruction_part, 8) + instruction
            address += 1

        # After the instruction has been fetched, I get the opcode to understand the type of the instruction (R-Type, I-Type...)
        return self.__get_instruction_object(instruction)
    

    def __get_instruction_object(self, instruction: str):
        opcode = instruction[0:6]
        funct = instruction[26:32]

        if opcode == '000000':
            # It is an R-Type instruction
            if funct == '001100':
                instruction_obj = SystemCallInstruction()
            elif funct == '001101':                 # It is a break instruction
                raise BreakException('Execution stopped using break instruction')
            else:
                rs = bits_to_int(instruction[6:11])
                rt = bits_to_int(instruction[11:16])
                rd = bits_to_int(instruction[16:21])
                shamt = bits_to_int(instruction[21:26])
                funct = bits_to_int(instruction[26:32])
                instruction_obj = RTypeInstruction(bits_to_int(opcode), rs, rt, rd, shamt, funct)
        elif opcode == '000100':
            # It is a BEQ instruction
            rs = bits_to_int(instruction[6:11])
            rt = bits_to_int(instruction[11:16])
            offset = bits_to_int(instruction[16:32])
            instruction_obj = BranchOnEqualInstruction(bits_to_int(opcode), rs, rt, offset)
        elif opcode == '000010':
            # It is a jump instruction
            target = bits_to_int(instruction[6:32])
            instruction_obj = JumpInstruction(target)
        else:
            # It is a I-Type instruction
            rs = bits_to_int(instruction[6:11])
            rt = bits_to_int(instruction[11:16])
            immediate = bits_to_int(instruction[16:32])
            instruction_obj = ITypeInstruction(bits_to_int(opcode), rs, rt, immediate)

        return instruction_obj


    def __decode_instruction(self, instruction: Instruction):
        if hasattr(instruction, 'rs') and hasattr(instruction, 'rt'):
            rs = instruction.rs
            rt = instruction.rt
            self.__A = self.__register_file.get_register(rs)
            self.__B = self.__register_file.get_register(rt)

        # I calculate the branch address, so if the instruction is a BEQ I already have it
        offset = str(instruction)[16:32]
        self.__alu.src_a = self.__PC
        self.__alu.src_b = bits_to_int(offset)
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
            pass
        elif isinstance(instruction, JumpInstruction):
            pass
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
        immediate = bits_to_int(str(instruction)[16:32])
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
            raise RuntimeError(f'Address {address} is not aligned to the word')
        
        if instruction.opcode == 0x23:
            # Load word
            memory_data = self.memory.get_data(address)
            self.register_file.write(memory_data, instruction.rt)
        else:
            # Store word
            data_to_write = self.register_file.get_register(instruction.rt)
            data_to_write_str = str(data_to_write)

            bytes = [
                data_to_write_str[24:32],
                data_to_write_str[16:24],
                data_to_write_str[8:16],
                data_to_write_str[0:8]
            ]

            for i in range(4):
                self.memory.write_data(bytes[i], address)
                address += 1