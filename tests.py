import unittest

from libs.Simulator import Simulator


class DatapathTest(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.simulator = Simulator()


class ITypeTests(DatapathTest):
    def test(self):
        self.simulator.instructions = [
            '00100001000010000000000000000001'          # addi $t0, $t0, 0x1
        ]
        self.simulator.run()
        t0_register = self.simulator.datapath.register_file.get_register(8)
        self.assertEqual(t0_register, 1)


class RTypeTests(DatapathTest):
    def test(self):
        self.simulator.instructions = [
            '00100001000010000000000000000001',         # addi $t0, $t0, 0x1
            '00000001000010000100100000100000'          # add $t1, $t0, $t0
        ]
        self.simulator.run()
        t1_register = self.simulator.datapath.register_file.get_register(9)
        self.assertEqual(t1_register, 2)


class LuiWordTest(DatapathTest):
    def test(self):
        self.simulator.instructions = [
            '00111100000010000001000000000000'          # lui $t0, 0x1000
        ]
        self.simulator.run()
        t0_register = self.simulator.datapath.register_file.get_register(8)
        self.assertEqual(t0_register, 0x10000000)


class MemoryTest(DatapathTest):
    def test(self):
        self.simulator.instructions = [
            '00111100000010000001000000000000',         # lui $t0, 0x1000
            '00100001000010000001000000000000',         # addi $t0, $t0, 0x1000
            '00100001001010010000000000000010',         # addi $t1, $t1, 0x2
            '10101101000010010000000000000000'          # sw $t1, 0x0($t0)
        ]
        self.simulator.run()
        t0_register = self.simulator.datapath.register_file.get_register(8)
        self.assertEqual(t0_register, 0x10001000)
        memory_content = self.simulator.datapath.memory.get_data(0x10001000)
        self.assertEqual(memory_content, 2)


if __name__ == '__main__':
    unittest.main()
