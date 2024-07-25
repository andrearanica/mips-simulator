#include <iostream>
#include <string>
#include <unordered_map>
using namespace std;

enum Phases { fetch, decode, execute };

class ControlUnit {
    private:
        unordered_map<string,int> build_fetch() {
            unordered_map<string,int> result;
            result["MemRead"] = true;
            result["ALUSrcA"] = 0;
            result["IorD"] = 0;
            result["IRWrite"] = 1;
            result["ALUSrcB"] = 1;
            result["ALUOp"] = 0;
            result["PCWrite"] = 1;
            result["PCSorce"] = 0;
            return result;
        }

        unordered_map<string,int> build_decode() {
            unordered_map<string,int> result;
            result["ALUSrcA"] = 0;
            result["ALUSrcB"] = 3;
            result["ALUOp"] = 0;
            return result;
        }

        unordered_map<string,int> build_execute() {
            unordered_map<string,int> result;
            // TODO
            return result;
        }

    public:
        virtual unordered_map<string,int> execute(int phase, int opcode) {
            // Depending on the opcode, the control unit will enable different components
            unordered_map<string,int> signals;
            switch(phase) {
                case fetch:
                    cout << "Fetching the instruction..." << endl;
                    signals = this->build_fetch();
                    break;
            }
            return signals;
        }
};