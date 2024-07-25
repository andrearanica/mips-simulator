#include <string>
using namespace std;

class Instruction {
    protected:
        int opcode;
    
    public:
        Instruction(int opcode) {
            this->opcode = opcode;
        }

        int getOpcode() {
            return this->opcode;
        }

        virtual int getRs() {
            return -1;
        }

        virtual int getRt() {
            return -1;
        }

        virtual int getRd() {
            return -1;
        }

        virtual int getFunct() {
            return -1;
        }

        virtual string toString() {
            return "";
        }
};

class RTypeInstruction : public virtual Instruction {
    private:
        int rs;
        int rt;
        int rd;
        int shamt;
        int funct;

    public:
        RTypeInstruction(int opcode, int rs, int rt, int rd, int shamt, int funct) : Instruction(opcode) {
            this->rs = rs;
            this->rt = rt;
            this->rd = rd;
            this->shamt = shamt;
            this->funct = funct;
        }

        int getRs() {
            return this->rs;
        }

        int getRt() {
            return this->rt;
        }

        int getRd() {
            return this->rd;
        }

        int getFunct() {
            return this->funct;
        }

        string toString() {
            bitset<6> opcode_bit = bitset<6>(opcode);
            bitset<5> rs_bit = bitset<5>(rs);
            bitset<5> rt_bit = bitset<5>(rt);
            bitset<5> rd_bit = bitset<5>(rd);
            bitset<6> funct_bit = bitset<6>(funct);
            return opcode_bit.to_string() + rs_bit.to_string() + rt_bit.to_string() + rd_bit.to_string() + funct_bit.to_string();
        }

        string toFormattedString() {
            string result = "";
            result += "opcode: " + to_string(this->opcode) + '\n';
            result += "rs: " + to_string(this->rs) + '\n';
            result += "rt: " + to_string(this->rt) + '\n';
            result += "rd: " + to_string(this->rd) + '\n',
            result += "funct: " + to_string(this->funct);
            return result;
        }
};