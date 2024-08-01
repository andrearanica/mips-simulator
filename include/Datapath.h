#include <string>
#include <vector>
#include <bitset>
#include <typeinfo>
#include <sstream>
#include "ALU.h"
#include "ControlUnit.h"
#include "Instruction.h"
#include "Memory.h"
#include "RegisterFile.h"
#include "utils.h"
using namespace std;

const int MEMORY_DIM = 2000000000;
const int MAX_INSTRUCTIONS = 1000;

const int TEXT_SEGMENT_START = 4194304;

const string EMPTY_INSTRUCTION = "00000000000000000000000000000000";

class Datapath {
    private:
        int PC, A, B, ALUOut;
        ALU alu;
        ControlUnit controlUnit;
        Memory memory;
        RegisterFile registerFile;

        void loadProgramInMemory(vector<bitset<32>> instructions) {
            // Each instruction takes 4 slots of the memory
            int addressToWrite = TEXT_SEGMENT_START;
            for (int i = 0; i < instructions.size(); i++) {
                bitset<32> instruction_bit = instructions.at(i);
                string instruction_str = instruction_bit.to_string();

                // These bytes represent the instruction divided in bytes
                vector<bitset<8>> bytes = {
                    bitset<8>(instruction_str.substr(24, 32)),
                    bitset<8>(instruction_str.substr(16, 24)),
                    bitset<8>(instruction_str.substr(8, 16)),
                    bitset<8>(instruction_str.substr(0, 8))
                };
                
                // I store in memory this data with little endian
                for(int i = 0; i < bytes.size(); i++) {
                    memory.setAddress(addressToWrite);
                    memory.setWriteData(bytes.at(i).to_ulong());
                    memory.write();
                    addressToWrite += 1;
                }
            }
        }

        Instruction* fetchInstruction() {
            // I load from the memory the int that represents the instruction
            int address = this->PC;
            string instruction_str = "";

            for(int i = 0; i < 4; i++) {
                memory.setAddress(address);
                int data = memory.getData();
                bitset<8> data_bit = bitset<8>(data);
                instruction_str = data_bit.to_string() + instruction_str;
                address++;
            }

            this->PC += 4;
            string opcode_str = instruction_str.substr(0, 6);
            string funct_str = instruction_str.substr(26, 32);
            bitset<6> opcode = bitset<6>(opcode_str); 

            Instruction* instruction;
            if (opcode_str == "000000") {
                if (funct_str == "001100") {
                    // SystemCall
                    instruction = new SystemCallInstruction();
                } else {
                    // R-Type instruction
                    bitset<5> rs = bitset<5>(instruction_str.substr(6, 11));
                    bitset<5> rt = bitset<5>(instruction_str.substr(11, 16));
                    bitset<5> rd = bitset<5>(instruction_str.substr(16, 21));
                    bitset<5> shamt = bitset<5>(instruction_str.substr(21, 26));
                    bitset<6> funct = bitset<6>(instruction_str.substr(26));
                    instruction = new RTypeInstruction(opcode.to_ulong(), rs.to_ulong(), rt.to_ulong(), rd.to_ulong(), shamt.to_ulong(), funct.to_ulong());
                }
            } else if (opcode_str == "000100") {
                // Branch on Equal instruction
                bitset<5> rs = bitset<5>(instruction_str.substr(6, 11));
                bitset<5> rt = bitset<5>(instruction_str.substr(11, 16));
                bitset<16> offset = bitset<16>(instruction_str.substr(16, 32));
                instruction = new BranchOnEqualInstruction(rs.to_ulong(), rt.to_ulong(), offset.to_ulong());
            } else {
                // I-Type instructions (the OPCODE is different for each instruction)
                bitset<5> rs = bitset<5>(instruction_str.substr(6, 11));
                bitset<5> rt = bitset<5>(instruction_str.substr(11, 16));
                bitset<16> immediate = bitset<16>(instruction_str.substr(16, 32));
                instruction = new ITypeInstruction(opcode.to_ulong(), rs.to_ulong(), rt.to_ulong(), immediate.to_ulong());
            }

            return instruction;
        }

        void decodeInstruction(Instruction* instruction) {
            // I put inside the registers A and B the values of $rs and $rt
            registerFile.setReadRegister1(instruction->getRs());
            registerFile.setReadRegister2(instruction->getRt());
            A = registerFile.getReadData1();
            B = registerFile.getReadData2();

            // I calculate the branch address as an offset (16 bit) of the current program counter and put it inside the ALUOut
            // TODO add negative jump
            alu.setSrcA(PC);
            bitset<16> offset = bitset<16>(instruction->toString().substr(16, 32));
            alu.setSrcB(offset.to_ulong());
            alu.setAluOperation(2);
            ALUOut = alu.getResult();
        }

        void executeInstruction(Instruction* instruction) {
            if (RTypeInstruction* i = dynamic_cast<RTypeInstruction*>(instruction)) {
                // I need to understand the type of the operation depending on the funct code
                alu.setSrcA(A);
                alu.setSrcB(B);
                switch(instruction->getFunct()) {
                    case 0x20:
                        alu.setAluOperation(SUM);
                        break;
                    case 0x22:
                        alu.setAluOperation(SUB);
                        break;
                    case 0x24:
                        alu.setAluOperation(AND);
                        break;
                    case 0x25:
                        alu.setAluOperation(OR);
                        break;
                    case 0x2a:
                        alu.setAluOperation(SLT);
                        break;
                    default:
                        throw NotValidInstructionException("Not valid instruction");
                        break;
                }
                int result = alu.getResult();
                writeResult(result, instruction->getRd());
            } else if (ITypeInstruction* i = dynamic_cast<ITypeInstruction*>(instruction)) {
                bool isMemoryInstruction = false;
                alu.setSrcA(A);
                // FIXME implement negative numbers
                bitset<16> immediate = bitset<16>(instruction->toString().substr(16, 32));
                alu.setSrcB(immediate.to_ulong());
                // I-Type instructions are different by the opcode
                switch(instruction->getOpcode()) {
                    // TODO remove numbers use enum
                    case 8:
                        // ADDI instruction
                        alu.setAluOperation(SUM);
                        break;
                    case 0xc:
                        // ANDI instruction
                        alu.setAluOperation(AND);
                        break;
                    case 0xd:
                        // ORI instruction
                        alu.setAluOperation(OR);
                        break;
                    case 0x23:
                        // Load word instruction
                        alu.setAluOperation(SUM);
                        isMemoryInstruction = true;
                        break;
                    case 0x2b:
                        // Store word instruction
                        alu.setAluOperation(SUM);
                        isMemoryInstruction = true;
                        break;
                    case 0xf:
                        // Load upper immediate instruction
                        alu.setShamt(16);
                        alu.setAluOperation(SLL);
                        break;
                    default:
                        throw NotValidInstructionException("Not valid instruction");
                        break;
                }
                // FIXME the result shoudl be written inside the ALUOut register
                int result = alu.getResult();
                // ALUOut = result;
                // If it is a memory instruction the result is the address of the memory in which do the stuff
                if (!isMemoryInstruction) {
                    writeResult(result, instruction->getRt());
                } else {
                    // I need to check if the address is valid (if it is aligned on the word)
                    if (!isAddressValid(result)) {
                        throw InvalidMemoryAccess("Address "+to_string(result)+" is not aligned");
                    }
                    if (instruction->getOpcode() == 0x23) {
                        // It is a load word instruction: I have to write inside the $rt register the content of the memory
                        memory.setAddress(result);
                        int memoryData = memory.getData();
                        registerFile.setWriteRegister(instruction->getRt());
                        registerFile.setWriteData(memoryData);
                        registerFile.write();
                    } else {
                        // It is a store word instruction
                        memory.setAddress(result);
                        registerFile.setReadRegister1(instruction->getRt());
                        int dataToWrite = registerFile.getReadData1();
                        memory.setWriteData(dataToWrite);
                        memory.write();
                    }
                }
            } else if (BranchOnEqualInstruction* i = dynamic_cast<BranchOnEqualInstruction*>(instruction)) {
                // Inside ALUOut I have the new PC if the two registers are equal
                alu.setSrcA(A);
                alu.setSrcB(B);
                alu.setAluOperation(6);
                if (alu.getResult() == 0) {
                    // The two registers are equal
                    this->PC = ALUOut;
                }
            } else if (SystemCallInstruction* i = dynamic_cast<SystemCallInstruction*>(instruction)) {
                registerFile.setReadRegister1(2);
                registerFile.setReadRegister2(4);
                int syscallType = registerFile.getReadData1();
                int param = registerFile.getReadData2();
                switch (syscallType) {
                    case 1: case 2: case 3:
                        // print int
                        cout << param << endl;
                        break;
                    case 4:
                        // TODO implement print string
                        break;
                    case 5: case 6: case 7:
                        int data;
                        cin >> data;
                        registerFile.setWriteRegister(4);
                        registerFile.setWriteData(data);
                        registerFile.write();
                        break;
                    case 8:
                        // TODO implement read string
                        break;
                }
            } else {
                throw NotValidInstructionException("Not valid instruction");
            }
        }

        void writeResult(int result, int rd) {
            registerFile.setWriteRegister(rd);
            registerFile.setWriteData(result);
            registerFile.write();
        }

        // returns True if the address ends with two zeros (so if it is aligned at the word)
        bool isAddressValid(int address) {
            bitset<32> address_bit = bitset<32>(address);
            string lastTwoBits = address_bit.to_string().substr(30, 32);
            return (lastTwoBits == "00");
        }

        void handle() {
            try {
                throw;
            } catch(OverflowException e) {
                cout << "Overflow exception detected and ignored" << endl;
            } catch(InvalidMemoryAccess e) {
                cout << "Invalid memory access exception detected and ignored" << endl;
            } catch(NotValidInstructionException e) {
                cout << "Not valid instruction exception detected and ignored" << endl;
            }
        }

    public:
        Datapath() : alu(), controlUnit(), memory(MEMORY_DIM) {
            PC = TEXT_SEGMENT_START;
        }

        void run(string program) {
            vector<string> instructions;
            stringstream programStream(program);
            string programRow = "";

            while (getline(programStream, programRow)) {
                instructions.push_back(programRow);
            }
            vector<bitset<32>> instructionsBit;            

            for(int i = 0; i < instructions.size(); i++) {
                bitset<32> instruction(instructions[i]);
                instructionsBit.push_back(instruction);
            }

            loadProgramInMemory(instructionsBit);
            
            registerFile.setReadRegister1(10);
            
            // FIXME not realistic and doesn't work with BEQ
            for(int i = 0; i < instructions.size(); i++) {
                Instruction* fetched_instruction = fetchInstruction();
                decodeInstruction(fetched_instruction);
                try {
                    executeInstruction(fetched_instruction);
                } catch(exception e) {
                    handle();
                }
            }
            
            cout << "Registers at the end of the execution" << endl << registerFile.toString() << endl;
        }
};