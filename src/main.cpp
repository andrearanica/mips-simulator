#include <iostream>
#include <fstream>
#include "../include/Datapath.h"
using namespace std;

int main() {
    Datapath* datapath = new Datapath();

    string filePath = "./program.txt";
    
    ifstream fileReader(filePath);
    string temp;
    string fileContent = "";
    while (getline(fileReader, temp)) {
        fileContent += temp + "\n";
    }

    datapath->run(fileContent);

    return 0;
}