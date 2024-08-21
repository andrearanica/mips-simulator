from constants import MIN_INT, MAX_INT

class Memory:
    def __init__(self, size: int) -> None:
        self.__size = size
        self.__data = []
    

    @property
    def write_data(self) -> int:
        return self.__write_data
    

    @write_data.setter
    def write_data(self, write_data: int) -> None:
        if write_data < MIN_INT or write_data > MAX_INT:
            raise OverflowError()
        self.__write_data = write_data


    def get_data(self, address: int) -> int:
        return self.__data[address]
    

    def write_data(self, data: int, address: int) -> None:
        self.data[address] = data


    def __str__(self) -> str:
        result = ""
        for i, memory_data in enumerate(self.data):
            if memory_data:
                result += f"{i} | {memory_data}"
        return result