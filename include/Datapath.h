#include "ALU.h"
#include "ControlUnit.h"
#include "Instruction.h"
#include "Memory.h"
#include "RegisterFile.h"
#include "utils.h"
#include <string>
#include <vector>
#include <bitset>
using namespace std;

const int MEMORY_DIM = 2000000000;
const int MAX_INSTRUCTIONS = 1000;

const int TEXT_SEGMENT_START = 4194304;

class Datapath {
    private:
        int PC, A, B;
        ALU* alu;
        ControlUnit* controlUnit;
        Memory* memory;
        RegisterFile* registerFile;

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
                    memory->setAddress(addressToWrite);
                    memory->setWriteData(bytes.at(i).to_ulong());
                    memory->write();
                    addressToWrite += 1;
                }
            }
        }

        void fetchInstruction() {
            // I load from the memory the int that represents the instruction
            int address = this->PC;
            string instruction_str = "";

            for(int i = 0; i < 4; i++) {
                memory->setAddress(address);
                int data = memory->getData();
                bitset<8> data_bit = bitset<8>(data);
                instruction_str = data_bit.to_string() + instruction_str;
                address++;
            }

            string opcode_str = instruction_str.substr(0, 6);
            cout << opcode_str << endl;
            
            Instruction instruction(10);

            this->PC += 4;
        }

    public:
        Datapath() {
            this->alu = new ALU();
            this->controlUnit = new ControlUnit();
            this->memory = new Memory(MEMORY_DIM);
            this->PC = TEXT_SEGMENT_START;
        }

        void run(string program) {
            vector<string> instructions = split_string(program, '\n');
            vector<bitset<32>> instructionsBit;
            
            for(int i = 0; i < instructions.size(); i++) {
                bitset<32> instruction(instructions[i]);
                instructionsBit.push_back(instruction);
            }

            loadProgramInMemory(instructionsBit);

            fetchInstruction();
        }
};