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
    for i, b in enumerate(bits[::-1]):
        n += int(b) * math.pow(2, i)
    return int(n)


def is_break_instruction(instruction: str) -> bool:
    return instruction[0:6] == '000000' and instruction[26:32] == '001101'


def is_valid_instruction(instruction: str) -> bool:
    return len(instruction) == 32


def is_address_valid(address: int) -> bool:
    """ Returns if the address is aligned to the word (last 00 bits)
    """
    address_in_bits = int_to_bits(address)
    return address_in_bits[len(address_in_bits)-2:len(address_in_bits)]


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