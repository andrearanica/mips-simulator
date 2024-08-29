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