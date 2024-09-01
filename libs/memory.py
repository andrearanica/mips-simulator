from libs.constants import MIN_INT, MAX_INT, DATA_SEGMENT_START, TEXT_SEGMENT_START

class Memory:
    def __init__(self) -> None:
        self.__text_segment = {}
        self.__data_segment = {}
        self.__stack_segment = {}

    @property
    def write_data(self) -> int:
        return self.__write_data

    @write_data.setter
    def write_data(self, write_data: int) -> None:
        if write_data < MIN_INT or write_data > MAX_INT:
            raise OverflowError()
        self.__write_data = write_data

    def get_data(self, address: int|None=None) -> int|dict:
        if address != None:
            if TEXT_SEGMENT_START <= address < DATA_SEGMENT_START:
                # Get data from text segment
                return self.__text_segment.get(address)
            elif DATA_SEGMENT_START <= address:
                # Get data from data segment
                return self.__data_segment.get(address)
            else:
                raise RuntimeError(f'Error trying to read memory address {address}')
        else:
            memory_dict = {}
            memory_dict.update(self.__text_segment)
            memory_dict.update(self.__data_segment)
            memory_dict.update(self.__stack_segment)
            return memory_dict

    def write_data(self, data: int, address: int) -> None:
        if TEXT_SEGMENT_START <= address < DATA_SEGMENT_START:
            # Write into text segment
            self.__text_segment[address] = data
        elif DATA_SEGMENT_START <= address:
            # Write into data segment
            self.__data_segment[address] = data
        else:
            raise RuntimeError(f'Address {address} is out of the memory limits')

    def __str__(self) -> str:
        # FIXME fix with dictionaries
        result = ""
        for i, memory_data in enumerate(self.data):
            if memory_data:
                result += f"{i} | {memory_data}"
        return result