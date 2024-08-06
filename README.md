# MIPS simulator

This software simulates the behaviour of the MIPS32 architecture with a multi-cycle datapath. The execution of a program is divided into different stages:
- Fetch: the CPU gets the instruction to execute from the memory
- Decode: the Control Unit understands what is the instruction type
- Execute: the CPU executes the instruction

## How to use?
This simulator takes a file made by 32-bits instructions organized in rows, like the following. *Important*: the last row of the file must be the `break` operation, to prevent the simulator to continue fetching the instruction from the memory.

``` assembly
00100001000010000000000000000001
00100001001010010000000000000001
00010001000010000000000000000100
00100001101011010000000100000000
00100000010000100000000000000001
00100000100001000000000100000000
00000000000000000000000000001100
00000000000000000000000000001101 --> break line
```

To get the binary rapresentation of an instruction you can use <a href="https://www.eg.bucknell.edu/~csci320/mips_web/">this</a> website.

### CMake
You need to run the following commands to get the executable file `build/mips-simulator`
``` bash
mkdir build
cd build
cmake ..
make
```

## Supported instructions
- R-Type: instructions that uses arithmetical-logical functions with registers (`add`, `sub`, `and`, `or`, `slt`)
- I-Type: instructions that manipulates registers using constant values (`addi`, `andi`, `ori`, `lw`, `sw`, `lui`)
- System calls: read and print numbers

## Components
The components that build a MIPS32 architecture are:
- ALU: the arithmetic logic unit executes the basic mathemathics operations, like sum or subtraction, and some logic operations, like slt
- Register file: contains the 32 general-purpose registers
- Memory: in the multi-cycle datapath, there is only a memory that contains both instructions and data
- Program Counter: a register that contains the address of the instruction to fetch from the memory
- Instruction Register: contains the instruction that has been fetched and can be read from the datapath

### ALU
Inputs:
- Two values for the operation
- ALU operation: depending on this value the ALU can make different operations:
    - 0000: AND
    - 0001: OR
    - 0010: ADD
    - 0110: SUB
    - 0111: SLT
    - 1100: NOR

Outputs:
- Zero: a bit that is 1 if the subtraction between the two values is zero
- ALU result: the result of the ALU operation

### Register File
The register file contains the 32 general purpose registers. It can read two registers and write one register in a single clock. 
Input:
- Read register 1 and 2: the index of the registers to read
- Write register: the index of the register to write
- Write data: the data to write in the register

Output:
- ReadData1 and ReadData2

### Memory
The memory contains both instructions and data. The memory follows this structure:

| Reserved (0x0 - 0x400000) |
| -------- |
| Text segment (0x400000 - 0x10000000) |
| Data segment (0x10000000 - 0x7FFFFFFC) |
| Stack segment (0x7FFFFFFC) |

Operations that work with memory use words, but the address of the memory refers to the byte; each word will use 4 cells of the memory, and the address of the word is the address of the first byte of the memory (little endian)

Input:
- Address: the address of the data to read
- Write data: data to write inside the memory

Output:
- MemData: the data read form the memory at the address


### Datapath
The datapath contains all the components written before. It will do the following operations:
- Fetch
    - Reads the instruction from the memory
    - Increments the program counter
- Decode
    - Loads inside A and B the value of the registers written inside the instruction
    - Calculates and puts inside the ALUOut register the branch address (to take if the instruction is a branch instruction and condition is true)
- Execute
    - Depending on the type of the instruction, it does different operations (sum, immediates...)
    - To understand if the instruction is a r-type, i-type, beq or lw/sw the software checks the opcode
        - if opcode == 0, r-type
        - if opcode == 4, beq
        - else, it is a i-type
            - if opcode == 0x2b, store word
            - if opcode == 0x23, load word
            - else, it is a normal I-type instruction
- Handle: if the execute phase throws an exception, the datapath must handle the exception and continue or exit the program