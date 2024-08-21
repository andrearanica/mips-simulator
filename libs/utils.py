def int_to_bits(n: int, n_ciphers: int=0) -> str:
    """ Returns the integer represented in binary as a string
    """
    binary_n = "{0:b}".format(n)
    while n_ciphers and len(binary_n) < n_ciphers:
        binary_n = "0"+binary_n
    return binary_n


def is_break_instruction(instruction: str):
    return instruction[0, 6] == '000000' and instruction[26, 32] == '001101'