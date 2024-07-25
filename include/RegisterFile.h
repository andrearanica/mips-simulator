#include <string>

const int N_REGISTERS = 32;

class RegisterFile {
    private:
        int registers[N_REGISTERS];
        int readRegister1;
        int readRegister2;
        int writeRegister;
        int writeData;

        void initializeRegisters() {
            for(int i = 0; i < N_REGISTERS; i++) {
                registers[i] = 0;
            }
        }

    public:
        RegisterFile() {
            readRegister1 = -1;
            readRegister2 = -1;
            writeRegister = -1;
            writeData = 0;
            initializeRegisters();
        }

        void setReadRegister1(int readRegister1) {
            this->readRegister1 = readRegister1;
        }

        void setReadRegister2(int readRegister2) {
            this->readRegister2 = readRegister2;
        }

        void setWriteRegister(int writeRegister) {
            this->writeRegister = writeRegister;
        }

        void setWriteData(int writeData) {
            this->writeData = writeData;
        }

        int getReadData1() {
            return registers[readRegister1];
        }

        int getReadData2() {
            return registers[readRegister2];
        }

        void write() {
            registers[writeRegister] = writeData;
        }

        std::string toString() {
            std::string registerFileStr = "";
            for(int i = 0; i < N_REGISTERS; i++) {
                registerFileStr += std::to_string(registers[i]) + ";";
            }
            return registerFileStr;
        }
};