# Constants that represent the min and max integer that can be represented
MAX_INT = 2147483647
MIN_INT = -2147483648

# Dimention of the datapath's memory
MEMORY_DIM = 20000000;

# Standard instructions
EMPTY_INSTRUCTION = "00000000000000000000000000000000";
BREAK_INSTRUCTION = "00000000000000000000000000001101";

# Start of the memory segment dedicated to the text (instructions)
TEXT_SEGMENT_START = 4194304;

# Number of registers of the processor
N_REGISTERS = 32