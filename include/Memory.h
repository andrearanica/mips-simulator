class Memory {
    private:
        int address;
        int writeData;
        int* data;
    
    public:
        Memory(int size) {
            // Size of the memory is in bytes
            this->address = 0;
            this->writeData = 0;
            this->data = new int[size];
        }

        void setAddress(int address) {
            this->address = address;
        }

        void setWriteData(int writeData) {
            this->writeData = writeData;
        }

        int getData() {
            return this->data[this->address];
        }
};