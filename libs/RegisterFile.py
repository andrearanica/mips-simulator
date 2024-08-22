from .constants import N_REGISTERS


class RegisterFile:
    def __init__(self) -> None:
        self.__registers = [0] * N_REGISTERS
        self.__initialize_registers()


    def __initialize_registers(self):
        for i in range(len(self.__registers)):
            self.__registers[i] = 0
    

    def get_register(self, register: int):
        if register < 0 or register > N_REGISTERS:
            raise RuntimeError(f'Register number {register} not valid, it should be a number between zero and {N_REGISTERS}')
        return self.__registers[register]

    def write(self, data: int, register: int):
        if register < 0 or register > N_REGISTERS:
            raise RuntimeError(f'Register number {register} not valid, it should be a number between zero and {N_REGISTERS}')
        self.__registers[register] = data
    
    def __str__(self) -> str:
        result = ''
        for register_number, register_value in enumerate(self.__registers):
            result += f'{register_number} | {register_value}\n'
        return result