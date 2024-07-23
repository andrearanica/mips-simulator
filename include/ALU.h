#include <iostream>

class ALU {
    private: 
        int srcA;
        int srcB;
        int aluOperation;

    public:
        ALU () {
            srcA = 0;
            srcB = 0;
            aluOperation = 0;
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

        int getResult() {
            int result = 0;
            switch(aluOperation) {
                case 0:
                    result = srcA & srcB;
                    break;
                case 1:
                    result = srcA | srcB;
                    break;
                case 2:
                    result = srcA + srcB;
                    break;
                case 6:
                    result = srcA - srcB;
                    break;
                case 7:
                    result = srcA < srcB;
                    break;
            }
            return result;
        }
};