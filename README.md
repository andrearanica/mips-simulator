# MIPS simulator

A Python simulator that executes assembly programs for the  [MIPS32 architecture](https://it.wikipedia.org/wiki/Architettura_MIPS)

## Quick setup

First you need to make sure you have the `tk` library installed on your PC

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

## How to contribute

Open a Pull Request and assign it to the mantainer; I'll give a look at it as soon as possible and give you a reply!

### I want to add a new instruction, how can I do it?

This software is divided in two parts: the `assembler`, that translates the instruction into his binary representation, and the `datapath`, that executes the instructions. So, if you want to add a new instruction you must add it both into the assembler and into the datapath.

*Please check the `TODO.md` file to see which instructions are currently missing and which ones need to be improved*
