#include <unordered_map>
#include <string>
using namespace std;

unordered_map<string,int> getOpCodes() {
    unordered_map<string,int> opcodes;

    opcodes["lw"] = 0;
    opcodes["sw"] = 0;

    return opcodes;
}