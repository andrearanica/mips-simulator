class Instruction {
    protected:
        int opcode;
    
    public:
        Instruction(int opcode) {
            this->opcode = opcode;
        }
};

class RTypeInstruction : Instruction {
    private:
        int rs;
        int rt;
        int rd;
        int funct;

    public:
        RTypeInstruction(int opcode, int rs, int rt, int rd, int funct) : Instruction(opcode) {
            this->rs = rs;
            this->rt = rt;
            this->rd = rd;
            this->funct = funct;
        }

        int getOpcode() {
            return this->opcode;
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
};