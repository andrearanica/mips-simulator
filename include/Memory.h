#include <string>
using namespace std;

class Memory {
    private:
        int address;
        int writeData;
        int* data;
        int size;
    
    public:
        Memory(int size) {
            // Size of the memory is in bytes
            this->address = 0;
            this->writeData = 0;
            this->data = new int[size];
            this->size = size;
        }

        void setAddress(int address) {
            this->address = address;
        }

        void setWriteData(int writeData) {
            this->writeData = writeData;
        }

        void write() {
            this->data[this->address] = this->writeData;
        }

        int getData() {
            return this->data[this->address];
        }

        string toString() {
            string result = "Memory content\n";
            for(int i = 0; i < size; i++) {
                if (this->data[i] != 0) {
                    result += "Address " + to_string(i) + ": " + bitset<8>(data[i]).to_string() + "\n";
                }
            }
            return result;
        }
};