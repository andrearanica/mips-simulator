# MIPS simulator

A Python simulator that executes assembly programs for the  [MIPS32 architecture](https://it.wikipedia.org/wiki/Architettura_MIPS)

## Quick setup

First you need to make sure you have the `tk` library installed on your PC.
After that, you can run the python script with the following command.

``` bash
cd path/to/project
python3 .
```

#### debian-based distros

``` bash
sudo apt install python3-tk
```

#### Windows

``` bash
pip install tk
```

## Usage

This software reads both .asm files (that contain assembly instuctions) and .o files (with binary instructions)

The instructions that are currently supported are the following:

- **R-Type**: `and`, `or`, `add`, `sub`, `slt`, `sll`
- **I-Type**: `andi`, `ori`, `addi`, `lw`, `sw`
- **Branches**: `beq`
- **Jumps**: `j`
- **Others**: `break`

**Important**: feel free to open a pull request to add new instructions

### Limitations
You cannot use the `.data` assembly segment, so you can't define labels or use assembler directives in this way.
```
.data
name: .asciiz "marco"

.text
lw $t0, 0(name)     -> this is not supported
loop:   addi $t0, $t0, 1
        beq $t0, $t1, loop    -> this is not supported
```

So, if you want to access memory using `lw/sw` you should store the address inside a register and then work with that memory address.
```
lui $t0, $t0, 1000
addi $t0, $t0, 1000
addi $t1, $t1, 5
sw $t1, 0($t0)
```

## How to contribute

Open a Pull Request and assign it to the mantainer; I'll give a look at it as soon as possible and give you a reply!

### I want to add a new instruction, how can I do it?

This software is divided in two parts: the `assembler`, that translates the instruction into his binary representation, and the `datapath`, that executes the instructions. So, if you want to add a new instruction you must add it both into the assembler and into the datapath.

*Please check the `TODO.md` file to see which instructions are currently missing and which ones need to be improved*
