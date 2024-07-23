#include "ALU.h"
#include "ControlUnit.h"
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

    public:
        Datapath() {
            this->alu = new ALU();
            this->controlUnit = new ControlUnit();
            this->memory = new Memory(MEMORY_DIM);
        }

        void run(string program) {
            vector<string> instructions = split_string(program, '\n');

            // Load in memory the instructions
            for(int i = 0; i < instructions.size(); i++) {
                bitset<32> instruction(instructions[i]);
                cout << instruction << endl;
            }
        }
};