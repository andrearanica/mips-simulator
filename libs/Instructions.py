from abc import ABC, abstractmethod
from .exceptions import NotValidInstructionException
from .utils import int_to_bits

# TODO implement MIN_INT and MAX_INT in setters


class Instruction(ABC):
    def __init__(self, opcode: int) -> None:
        self._opcode = opcode


    @property
    def opcode(self) -> int:
        return self._opcode
    

    @opcode.setter
    def opcode(self, opcode: int) -> None:
        self._opcode = opcode


class RegisterInstruction(Instruction):
    """ Abstract class that represents an instruction that uses registers
    """
    def __init__(self, opcode: int, rs: int, rt: int) -> None:
        super().__init__(opcode)
        self._rs = rs
        self._rt = rt
    

    @property
    def rs(self) -> int:
        return self._rs
    

    @rs.setter
    def rs(self, rs: int) -> None:
        if rs < 0 or rs > 31:
            raise NotValidInstructionException(f"Register {rs} is not a valid register")
        self._rs = rs
    

    @property
    def rt(self) -> int:
        return self._rt
    

    @rt.setter
    def rt(self, rt: int):
        if rt < 0 or rt > 31:
            raise NotValidInstructionException(f"Register {rt} is not a valid register")
        self._rs = rt


class RTypeInstruction(RegisterInstruction):
    """ Instruction that can executes logic and arithmetic functions on registers
    """
    def __init__(self, opcode: int, rs: int, rt: int, rd: int, shamt: int, funct: int) -> None:
        super().__init__(opcode, rs, rt)
        self._rd = rd
        self._shamt = shamt
        self._funct = funct
    

    @property
    def rd(self) -> int:
        return self._rd


    @rd.setter
    def rd(self, rd: int) -> None:
        if rd < 0 or rd > 31:
            raise RuntimeError(f"Register {rd} is not a valid register")
    

    @property
    def shamt(self) -> int:
        return self._shamt
    

    @shamt.setter
    def shamt(self, shamt: int) -> None:
        self._shamt = shamt


    @property
    def funct(self) -> int:
        return self._funct
    

    @funct.setter
    def funct(self, funct: int) -> None:
        self._funct = funct


    def __str__(self) -> str:
        return f"{int_to_bits(self.opcode, 6)}{int_to_bits(self.rs, 5)}{int_to_bits(self.rt, 5)}{int_to_bits(self.rd, 5)}{int_to_bits(self.shamt, 5)}{int_to_bits(self.funct, 6)}"


class ITypeInstruction(RegisterInstruction):
    """ Instruction that executes arithmetic and logical operations between registers and immediates
    """
    def __init__(self, opcode: int, rs: int, rt: int, immediate: int) -> None:
        super().__init__(opcode, rs, rt)
        self._immediate = immediate


    @property
    def immediate(self) -> int:
        return self._immediate
    

    @immediate.setter
    def immediate(self, immediate: int) -> None:
        self._immediate = immediate
    

    def __str__(self) -> str:
        return f"{int_to_bits(self.opcode, 6)}{int_to_bits(self.rs, 5)}{int_to_bits(self.rt, 5)}{int_to_bits(self.immediate, 16)}"


class BranchOnEqualInstruction(RegisterInstruction):
    """ Instruction that confront the content of two registers and jumps to an offset
    """
    def __init__(self, opcode: int, rs: int, rt: int, offset: int) -> None:
        super().__init__(opcode, rs, rt)
        self._offset = offset
    

    @property
    def offset(self) -> int:
        return self._offset
    

    @offset.setter
    def offset(self, offset: int) -> None:
        self._offset = offset


    def __str__(self) -> str:
        return f"{int_to_bits(self.opcode, 6)}{int_to_bits(self.rs, 5)}{int_to_bits(self.rt, 5)}{int_to_bits(self.offset, 16)}"


class JumpInstruction(Instruction):
    """ Instruction that jumps inconditionally to a target
    """
    def __init__(self, target: int) -> None:
        super().__init__(2)
        self._target = target
    

    @property
    def target(self) -> int:
        return self._target
    

    @target.setter
    def target(self, target: int) -> None:
        self._target = target
    

    def __str__(self) -> str:
        return f"000010{int_to_bits(self.target, 26)}"
    

class SystemCallInstruction(Instruction):
    """ Instruction that calls the system basic functions
    """
    def __init__(self) -> None:
        super().__init__(0)
    
    
    def __str__(self) -> str:
        return "00000000000000000000000000001100"