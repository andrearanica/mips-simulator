from enum import Enum

class Systems(Enum):
    BINARY = 2
    DECIMAL = 10
    HEX = 16

# Constants that represent the min and max integer that can be represented
MAX_INT = 2147483647
MIN_INT = -2147483648

# Dimention of the datapath's memory
MEMORY_DIM = 2147483644;

# Standard instructions
EMPTY_INSTRUCTION = "00000000000000000000000000000000";
BREAK_INSTRUCTION = "00000000000000000000000000001101";

# Start of the memory segment dedicated to the text (instructions)
TEXT_SEGMENT_START = 0x400000
DATA_SEGMENT_START = 0x10000000

# Number of registers of the processor
N_REGISTERS = 32

REGISTERS_NAMES = {
    0: "$zero",
    1: "$at",
    2: "$v0",
    3: "$v1",
    4: "$a0",
    5: "$a1",
    6: "$a2",
    7: "$a3",
    8: "$t0",
    9: "$t1",
    10: "$t2",
    11: "$t3",
    12: "$t4",
    13: "$t5",
    14: "$t6",
    15: "$t7",
    16: "$s0",
    17: "$s1",
    18: "$s2",
    19: "$s3",
    20: "$s4",
    21: "$s5",
    22: "$s6",
    23: "$s7",
    24: "$t8",
    25: "$t9",
    26: "$k0",
    27: "$k1",
    28: "$gp",
    29: "$sp",
    30: "$fp",
    31: "$ra"
}

RTYPE_OPCODE = 0x0

RTYPE_OPCODES = {
    'add': 0x0,
    'and': 0x0,
    'nor': 0x0,
    'or': 0x0,
    'sll': 0x0,
    'sub': 0x0,
    'slt': 0x0
}

ITYPE_OPCODES = {
    'addi': 0x8,
    'andi': 0xc,
    'ori': 0xd,
    'lui': 0xf,
    'beq': 0x4
}

JUMP_OPCODES = {
    'j': 0x2,
    'jal': 0x3
}

MEMORY_OPCODES = {
    'lw': 0x23,
    'sw': 0x2b
}

OPCODES = {}
OPCODES.update(RTYPE_OPCODES)
OPCODES.update(ITYPE_OPCODES)
OPCODES.update(JUMP_OPCODES)
OPCODES.update(MEMORY_OPCODES)

FUNCT_CODES = {
    'add': 0x20,
    'and': 0x24,
    'nor': 0x27,
    'or': 0x25,
    'sll': 0x0,
    'sub': 0x22,
    'slt': 0x2a
}