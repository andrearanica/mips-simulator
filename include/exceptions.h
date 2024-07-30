#include <stdexcept>
using namespace std;

class OverflowException : public runtime_error {
    public:
        OverflowException(string message) : runtime_error(message) {}
};

class InvalidMemoryAccess : public runtime_error {
    public:
        InvalidMemoryAccess(string message) : runtime_error(message) {}
};

class NotValidInstructionException : public runtime_error {
    public:
        NotValidInstructionException(string message) : runtime_error(message) {}
};