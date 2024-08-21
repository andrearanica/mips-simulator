from AluOperations import AluOperations
from constants import MAX_INT, MIN_INT
from exceptions import NotValidInstructionException

class ALU:
    def __init__(self) -> None:
        self.__src_a = 0
        self.__src_b = 0
        self.__alu_operation = 0
        self.__shamt = 0
    

    @property
    def src_a(self) -> int:
        return self.__src_a
    

    @src_a.setter
    def src_a(self, src_a):
        if not src_a in getattr(AluOperations):
            raise NotValidInstructionException("Not valid ALU operation")
        self.src_a = src_a


    @property
    def src_b(self) -> int:
        return self.__src_b


    @src_b.setter
    def src_b(self, src_b):
        if not src_b in getattr(AluOperations):
            raise NotValidInstructionException("Not valid ALU operation")
        self.src_b = src_b


    def set_src_a(self, src_a: int) -> None:
        self.__src_a = src_a
    

    def set_src_b(self, src_b: int) -> None:
        self.__src_b = src_b
    

    def set_alu_operation(self, alu_operation: int) -> None:
        self.__alu_operation = alu_operation
    

    def set_shamt(self, shamt: int) -> None:
        self.__shamt = shamt
    
    
    def getResult(self) -> int:
        """ Returns the result of the set operation
        """
        result = 0
        if self.__alu_operation == AluOperations.AND:
            result = self.__src_a & self.__src_b
        elif self.__alu_operation == AluOperations.OR:
            result = self.__src_a | self.__src_b
        elif self.__alu_operation == AluOperations.SUM:
            if self.__src_a > MAX_INT - self.__src_b: # I check if there is an overflow
                raise OverflowError(f"Overflow computing {self.__src_a}+{self.__src_b}")
            result = self.__src_a + self.__src_b
        elif self.__alu_operation == AluOperations.SUB:
            if self.__src_a < MIN_INT + self.__src_b:
                raise OverflowError(f"Overflow computing {self.__src_a}-{self.__src_b}")
            result = self.__src_a - self.__src_b
        elif self.__alu_operation == AluOperations.SLT:
            result = self.__src_a < self.__src_b
        elif self.__alu_operation == AluOperations.SLL:
            result = self.__src_b << self.__shamt
        else:
            raise NotValidInstructionException()
        
        return result