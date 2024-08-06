#include <iostream>
#include <fstream>
#include "../include/Datapath.h"
using namespace std;

int main(int argc, char* argv[]) {
    Datapath* datapath = new Datapath();
    string filePath = "";
    if (argc >= 2) {
        filePath = argv[1];
    } else {
        cout << "Insert file path: ";
        cin >> filePath;
    }
    
    ifstream fileReader(filePath);
    string temp;
    string fileContent = "";
    while (getline(fileReader, temp)) {
        fileContent += temp + "\n";
    }

    cout << filePath << endl;

    datapath->run(fileContent);

    return 0;
}