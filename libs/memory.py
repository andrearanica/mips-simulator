from libs import utils
from libs.exceptions import NotValidMemoryAddressException
from libs.constants import MIN_INT, MAX_INT, DATA_SEGMENT_START, TEXT_SEGMENT_START
from libs.exceptions import NotValidMemoryAddressException

class Memory:
    def __init__(self) -> None:
        self.__text_segment = {}
        self.__data_segment = {}
        self.__stack_segment = {}

    def get_data(self, address: int|None=None) -> int|dict:
        if address != None:
            if TEXT_SEGMENT_START <= address < DATA_SEGMENT_START:
                # Get data from text segment
                read_data = self.__text_segment.get(address)
            elif DATA_SEGMENT_START <= address:
                # Get data from data segment
                read_data = self.__data_segment.get(address)
            else:
                raise NotValidMemoryAddressException(f'Error trying to read memory address {address}')
            if read_data != None:
                return read_data
            else:
                return 0
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

    def write_word_data(self, data: int, address: int) -> None:
        """ Writes data in memory using 4 groups of bytes
        """
        data_str = utils.int_to_bits(data, 32, True)
        data_bytes = [
            utils.bits_to_int(data_str[24:32]),
            utils.bits_to_int(data_str[16:24]),
            utils.bits_to_int(data_str[8:16]),
            utils.bits_to_int(data_str[0:8])
        ]

        for i in range(4):
            self.write_data(data_bytes[i], address)
            address += 1

    def __str__(self) -> str:
        result = ""
        all_memory = {}
        all_memory.update(self.__text_segment)
        all_memory.update(self.__data_segment)
        for address, value in all_memory.items():
            result += f'{address} | {value}\n'
        return result