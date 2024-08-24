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
        self.assertTrue(t0_register == 1)

class RTypeTests(DatapathTest):
    def test(self):
        self.simulator.instructions = [
            '00100001000010000000000000000001',         # addi $t0, $t0, 0x1
            '00000001000010000100100000100000'          # add $t1, $t0, $t0
        ]
        self.simulator.run()
        t1_register = self.simulator.datapath.register_file.get_register(9)
        self.assertTrue(t1_register == 2)


class LuiWordTest(DatapathTest):
    def test(self):
        self.simulator.instructions = [
            '00111100000010000001000000000000'          # lui $t0, 0x1000
        ]
        self.simulator.run()

if __name__ == '__main__':
    unittest.main()
