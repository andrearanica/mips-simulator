#include <string>
#include <vector>
#include <bitset>
#include <typeinfo>
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
            bitset<6> opcode = bitset<6>(opcode_str); 

            Instruction* instruction;
            if (opcode_str == "000000") {
                bitset<5> rs = bitset<5>(instruction_str.substr(6, 11));
                bitset<5> rt = bitset<5>(instruction_str.substr(11, 16));
                bitset<5> rd = bitset<5>(instruction_str.substr(16, 21));
                bitset<5> shamt = bitset<5>(instruction_str.substr(21, 26));
                bitset<6> funct = bitset<6>(instruction_str.substr(26));
                instruction = new RTypeInstruction(opcode.to_ulong(), rs.to_ulong(), rt.to_ulong(), rd.to_ulong(), shamt.to_ulong(), funct.to_ulong());
            } else {
                // TODO j-type instructions and memory instructions
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
                        alu.setAluOperation(2);
                        break;
                    case 0x22:
                        alu.setAluOperation(6);
                        break;
                    case 0x24:
                        alu.setAluOperation(0);
                        break;
                    case 0x25:
                        alu.setAluOperation(1);
                        break;
                    case 0x2a:
                        alu.setAluOperation(7);
                        break;
                }
                int result = alu.getResult();
                cout << "Result: " << result << endl;
                // I have to write the result of the operation to the destination register
            } else {
                // TODO implement i-type and jumps
            }
        }

    public:
        Datapath() : alu(), controlUnit(), memory(MEMORY_DIM) {
            PC = TEXT_SEGMENT_START;
        }

        void run(string program) {
            vector<string> instructions = split_string(program, '\n');
            vector<bitset<32>> instructionsBit;
            
            for(int i = 0; i < instructions.size(); i++) {
                bitset<32> instruction(instructions[i]);
                instructionsBit.push_back(instruction);
            }

            loadProgramInMemory(instructionsBit);

            registerFile.setReadRegister1(10);
            cout << registerFile.getReadData1() << endl;

            Instruction* fetched_instruction = fetchInstruction();
            decodeInstruction(fetched_instruction);
            executeInstruction(fetched_instruction);
        }
};