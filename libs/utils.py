from libs import constants

import math

def int_to_bits(n: int, n_ciphers: int=0) -> str:
    """ Returns the integer represented in binary as a string
    """
    binary_n = "{0:b}".format(n)
    while n_ciphers and len(binary_n) < n_ciphers:
        binary_n = "0"+binary_n
    return binary_n

def bits_to_int(bits: str) -> int:
    """ Returns the integer represented by the passed string
    """
    n = 0
    sign = 1
    if bits[0] == '-':
        bits = bits[1:]
        sign = -1
    for i, b in enumerate(bits[::-1]):
        n += int(b) * math.pow(2, i)
    return sign*int(n)

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

def convert(number: int, system: int, n_ciphers=0) -> int:
    """ Converts the number from the decimal system to the desired one
    """
    if number == 0:
        return 0

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