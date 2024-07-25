#include <iostream>
#include <string>
#include <vector>
#include <bitset>
#include <math.h>
#include <unordered_map>
using namespace std;

vector<string> split_string(string stringToSplit, char delimiter) {
    vector<string> strings;
    int nStrings = 0;
    for(int i = 0; i < stringToSplit.length(); i++) {
        if (stringToSplit[i] == delimiter) {
            string newString = stringToSplit.substr(0, i);
            strings.push_back(newString);
            stringToSplit = stringToSplit.substr(i+1);
            nStrings++;
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