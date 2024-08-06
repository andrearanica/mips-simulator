#include <gtest/gtest.h>
#include "../include/Datapath.h"

// ADDI test
TEST(TEST_SUITE, addiTest) {
    // addi $t0, $t0, 0x1
    string program = "00100001000010000000000000000001";
    Datapath* datapath = new Datapath();
    datapath->run(program);

    RegisterFile registerFile = datapath->getRegisterFile();
    registerFile.setReadRegister1(8);
    int t0_value = registerFile.getReadData1();

    GTEST_ASSERT_EQ(t0_value, 1);
}

// SW test
TEST(TEST_SUITE, swTest) {
    // lui $t0, $t0, 0x1000
    // addi $t1, $t1, 0x10
    // sw $t1, 0x0($t0)
    string program = "00111100000010000001000000000000\n00100001001010010000000000010000\n10101101000010010000000000000000";
    Datapath* datapath = new Datapath();
    datapath->run(program);

    Memory memory = datapath->getMemory();
    memory.setAddress(0x10000000);
    int memoryContent = memory.getData();

    GTEST_ASSERT_EQ(memoryContent, 0x10);
}

int main() {
    ::testing::InitGoogleTest();
    return RUN_ALL_TESTS();
}