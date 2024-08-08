#include <iostream>
#include <fstream>
#include <filesystem>
#include "../include/Datapath.h"
using namespace std;

class MipsSimulator {
    private:
        Datapath datapath;
        string file_path = "";

        bool file_exists(string file_path) {
            ifstream file(file_path);
            return file.is_open();
        }

    public:
        MipsSimulator(string file_path) {
            this->file_path = file_path;
        }

        void run() {
            if (!file_exists(file_path)) {
                throw new ProgramException("File " + file_path + " not found");
            }

            ifstream file_reader(file_path);
            string temp;
            string file_content = "";
            while (getline(file_reader, temp)) {
                file_content += temp + "\n";
            }

            vector<string> instructions;
            stringstream programStream(file_content);
            string programRow = "";

            while (getline(programStream, programRow)) {
                instructions.push_back(programRow);
            }

            datapath.run(instructions);
        }
};

/*PYBIND11_MODULE(simulator, handle) {
    handle.doc() = "MIPS simulator";
    handle.def() = 
}*/

int main(int argc, char* argv[]) {
    Datapath* datapath = new Datapath();
    string file_path = "";
    if (argc >= 2) {
        file_path = argv[1];
    } else {
        cout << "Insert file path: ";
        cin >> file_path;
    }
    
    MipsSimulator simulator(file_path);

    simulator.run();

    return 0;
}