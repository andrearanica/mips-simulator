#include <iostream>

enum AluOperations { AND, OR, SUM, SUB, SLT, SLL, SRL };

class ALU {
    private: 
        int srcA;
        int srcB;
        int aluOperation;
        int shamt;

    public:
        ALU () {
            srcA = 0;
            srcB = 0;
            aluOperation = 0;
            shamt = 0;
        }

        void setSrcA(int srcA) {
            this->srcA = srcA;
        }

        void setSrcB(int srcB) {
            this->srcB = srcB;
        }

        void setAluOperation(int aluOperation) {
            this->aluOperation = aluOperation;
        }

        void setShamt(int shamt) {
            this->shamt = shamt;
        }

        int getResult() {
            int result = 0;
            switch(aluOperation) {
                case AND:
                    result = srcA & srcB;
                    break;
                case OR:
                    result = srcA | srcB;
                    break;
                case SUM:
                    result = srcA + srcB;
                    break;
                case SUB:
                    result = srcA - srcB;
                    break;
                case SLT:
                    result = srcA < srcB;
                    break;
                case SLL:
                    result = srcB << shamt;
                    break;
            }
            return result;
        }
};