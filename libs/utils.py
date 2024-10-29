from libs import constants

import math

def int_to_bits(value: int, bits: int=0, ca2: bool=False):
    if not ca2 or value >= 0:
        return bin(abs(value))[2:].zfill(bits)
    else:
        return bin((1 << bits) + value)[2:]

def bits_to_int(bits: str, ca2: bool=False) -> int:
    """ Returns the integer represented by the passed string
    """
    n = 0
    if not ca2 or bits[0] == '0':
        # It's a positive number
        for i, b in enumerate(bits[::-1]):
            n += int(b) * math.pow(2, i)
    else:
        # It's a negative number
        inv = ''.join('1' if b == '0' else '0' for b in bits)
        n = -1*(int(inv, 2)+1)
    return int(n)

def is_break_instruction(instruction: str) -> bool:
    return instruction[0:6] == '000000' and instruction[26:32] == '001101'

def is_valid_instruction(instruction: str) -> bool:
    return len(instruction) == 32

def is_address_valid(address: int) -> bool:
    """ Returns if the address is aligned to the word (last 00 bits)
    """
    address_in_bits = int_to_bits(address)
    return address_in_bits[len(address_in_bits)-2:len(address_in_bits)] == '00'

def is_binary_program_valid(program: str) -> bool:
    """ Returns if the passed binary program (composed only by 0s and 1s) is valid or not
    """
    return len(program) % 2 == 0 and program.isdigit()

def split_program_to_instructions(program: str) -> list:
    """ Returns a list of instruction as strings
    """
    instructions = []
    while program:
        instructions.append(program[0:32])
        program = program[32:]
    return instructions

def convert(number: int, system: int, n_ciphers:int=0, care_sign=False) -> int:
    """ Converts the number from the decimal system to the desired one
    """
    if number == 0:
        return 0
    
    if system == constants.Systems.DECIMAL.value:
        return number
    elif system == constants.Systems.BINARY.value:
        return int_to_bits(number, 32, True)
    else:
        converted_number = ''

        while number != 0:
            rest = normalize_cipher(int(number % system))
            converted_number += rest
            number = int(number / system)
        
        converted_number = converted_number[::-1]
        while n_ciphers and len(converted_number) < n_ciphers:
            converted_number = '0' + converted_number

        return converted_number

def normalize_cipher(n: int):
    a_char = ord('A')
    if n < 10:
        return str(n)
    else:
        return chr(a_char + (n-10))
    
def get_register_number_from_name(register_name: str):
    for number, name in constants.REGISTERS_NAMES.items():
        if name == register_name:
            return number
    return -1

def is_number(number_str: str):
    if not number_str[0].isnumeric():
        if not number_str[0] == '+' and not number_str[0] == '-':
            return False
        number_str = number_str[1:]
    return number_str.isnumeric()