#include <gtest/gtest.h>
#include "../include/Datapath.h"

// ADDI test
TEST(TEST_SUITE, addiTest) {
    // addi $t0, $t0, 0x1
    vector<string> program({"00100001000010000000000000000001"});
    Datapath* datapath = new Datapath();
    datapath->run(program);

    RegisterFile registerFile = datapath->getRegisterFile();
    registerFile.setReadRegister1(8);
    int t0_value = registerFile.getReadData1();

    GTEST_ASSERT_EQ(t0_value, 1);
}

// SW & LW test
TEST(TEST_SUITE, swTest) {
    string lui =  "00111100000010000001000000000000";       // lui $t0, $t0, 0x1000
    string lui1 = "00111100000010011010101010101010";       // lui $t1, $t1, 0xAAAA
    string addi = "00100001001010011010101010101010";       // addi $t1, $t1, 0xAAAA
    string sw =   "10101101000010010000000000000000";       // sw $t1, 0x0($t0)
    string lw =   "10001101000010100000000000000000";       // lw $t2, 0x0($t0)
    vector<string> program({lui, lui1, addi, sw, lw});
    Datapath* datapath = new Datapath();
    datapath->run(program);

    Memory memory = datapath->getMemory();
    memory.setAddress(0x10000002);
    int memoryContent = memory.getData();

    RegisterFile registerFile = datapath->getRegisterFile();
    registerFile.setReadRegister1(10);
    int t2_content = registerFile.getReadData1();

    GTEST_ASSERT_EQ(memoryContent, 0xAA);   // I check that in the memory I stored the number
    GTEST_ASSERT_EQ(t2_content, 0xAA);      // I check that the content of the memory has been loaded correctly
}

// BEQ test
TEST(TEST_SUITE, beqTest) {
    string addi1 = "00100001000010000000000000000001";      // addi $t0, $t0, 0x1
    string addi2 = "00100001001010010000000000000001";      // addi $t1, $t1, 0x1
    string beq =   "00010001000010010000000000000100";      // beq $t0, $t1, 0x4
    string addi =  "00100001010010100000000000010000";      // addi $t2, $t2, 0x10
    vector<string> program({addi1, addi2, beq, addi});

    Datapath* datapath = new Datapath();
    datapath->run(program);

    RegisterFile registerFile = datapath->getRegisterFile();
    registerFile.setReadRegister1(10);
    int t2_value = registerFile.getReadData1();

    GTEST_ASSERT_EQ(t2_value, 0);                           // $t2 must be zero because the addi has been skipped
}

// SLT test
TEST(TEST_SUITE, sltTest) {
    string addi = "00100001000010000000000000000001";   // addi $t0, $t0, 0x1
    string addi1 = "00100001001010010000000000000010";  // addi $t1, $t1, 0x2
    string slt = "00000001000010010101000000101010";    // slt $t2, $t0, $t1
    vector<string> program({addi, addi1, slt});

    Datapath* datapath = new Datapath();
    datapath->run(program);

    RegisterFile registerFile = datapath->getRegisterFile();
    registerFile.setReadRegister1(10);
    int t2_value = registerFile.getReadData1();

    GTEST_ASSERT_TRUE(t2_value); 
}

int main() {
    ::testing::InitGoogleTest();
    return RUN_ALL_TESTS();
}