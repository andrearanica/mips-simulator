#include <iostream>
#include <string>
#include <vector>
#include <bitset>
#include <math.h>
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