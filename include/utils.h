#include <iostream>
#include <string>
#include <vector>
#include <bitset>
#include <math.h>
#include <unordered_map>
using namespace std;

vector<string> split_string(string stringToSplit, char delimiter) {
    vector<string> strings;

    for(int i = 0; i < stringToSplit.length(); i++) {
        if (stringToSplit.at(i) == delimiter) {
            cout << stringToSplit << endl;
            string newString = stringToSplit.substr(0, i);
            strings.push_back(newString);
            stringToSplit = stringToSplit.substr(i+1);
        }
    }
    
    if (stringToSplit != "") {
        strings.push_back(stringToSplit);
    }

    return strings;
}

// R-Type operations are distinguished using the last 6 bits, that are funct codes
void getOperationType(int functCode) {
    unordered_map<int, string> functCodes;
    functCodes[0x20] = "add";
    functCodes[0x24] = "and";
    functCodes[0x18] = "mult";
    functCodes[0x27] = "nor";
    functCodes[0x25] = "or";
    functCodes[0x22] = "sub";
    // TODO add other operations
}

void printHeader() {
    cout << "-------------------------" << endl;
    cout << "|    MIPS SIMULATOR     |" << endl;
    cout << "-------------------------" << endl;
}

bool isBreakInstruction(bitset<32> instruction) {
    string instruction_str = bitset<32>(instruction).to_string();
    return instruction_str.substr(0, 6) == "000000" && instruction_str.substr(26, 32) == "001101";
}