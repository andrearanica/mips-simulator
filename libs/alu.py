from libs.alu_operations import AluOperations
from libs.constants import MAX_INT, MIN_INT
from libs.exceptions import NotValidInstructionException

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
    def src_a(self, src_a) -> None:
        self.__src_a = src_a

    @property
    def src_b(self) -> int:
        return self.__src_b

    @src_b.setter
    def src_b(self, src_b: int) -> None:
        self.__src_b = src_b

    @property
    def alu_operation(self) -> int:
        return self.__alu_operation

    @alu_operation.setter
    def alu_operation(self, alu_operation: int) -> None:
        # FIXME check if the operation is inside AluOperations
        self.__alu_operation = alu_operation
    
    @property
    def shamt(self) -> int:
        return self.__shamt
    
    @shamt.setter
    def shamt(self, shamt: int) -> None:
        self.__shamt = shamt

    @property
    def zero(self) -> int:
        return (self.src_a - self.src_b) == 0
    
    def get_result(self) -> int:
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