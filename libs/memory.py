from libs.constants import MIN_INT, MAX_INT, DATA_SEGMENT_START, TEXT_SEGMENT_START

class Memory:
    def __init__(self) -> None:
        self.__text_segment = []
        self.__data_segment = []
        self.__stack_segment = []

    @property
    def write_data(self) -> int:
        return self.__write_data

    @write_data.setter
    def write_data(self, write_data: int) -> None:
        if write_data < MIN_INT or write_data > MAX_INT:
            raise OverflowError()
        self.__write_data = write_data

    def get_data(self, address: int) -> int:
        # FIXME use a dictionary instead of lists
        if TEXT_SEGMENT_START <= address < DATA_SEGMENT_START:
            # Get data from text segment
            local_address = address-TEXT_SEGMENT_START
            return self.__text_segment[local_address]
        elif DATA_SEGMENT_START <= address:
            # Get data from data segment
            local_address = address-DATA_SEGMENT_START
            return self.__data_segment[local_address]
        return self.__data_segment[address-DATA_SEGMENT_START]
    
    def write_data(self, data: int, address: int) -> None:
        if TEXT_SEGMENT_START <= address < DATA_SEGMENT_START:
            # Write into text segment
            local_address = address - TEXT_SEGMENT_START
            while local_address >= len(self.__text_segment):
                self.__text_segment.append(0)
            self.__text_segment[local_address] = data
        elif DATA_SEGMENT_START <= address:
            # Write into data segment
            local_address = address - DATA_SEGMENT_START
            while local_address >= len(self.__data_segment):
                self.__data_segment.append(0)
            self.__data_segment[local_address] = data
        else:
            raise RuntimeError(f'Address {address} is out of the memory limits')

    def __str__(self) -> str:
        result = ""
        for i, memory_data in enumerate(self.data):
            if memory_data:
                result += f"{i} | {memory_data}"
        return result