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


def is_break_instruction(instruction: str):
    return instruction[0:6] == '000000' and instruction[26:32] == '001101'


def is_valid_instruction(instruction: str):
    return len(instruction) == 32


def is_address_valid(address: int):
    """ Returns if the address is aligned to the word (last 00 bits)
    """
    address_in_bits = int_to_bits(address)
    return address_in_bits[len(address_in_bits-2):len(address_in_bits)]