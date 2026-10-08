import unittest

from src.lth05.model import Instruction, ProgramCode
from src.lth05.vm import VirtualMachine


class LTH05VMTest(unittest.TestCase):
    def test_stack_execution(self):
        code = ProgramCode(
            instructions=[
                Instruction("CONST", 0),
                Instruction("CONST", 1),
                Instruction("BINARY", "+"),
                Instruction("STORE", 0),
                Instruction("HALT"),
            ],
            constants=[20, 22],
            names=["answer"],
        )

        result = VirtualMachine().run(code)

        self.assertEqual(result.values["answer"], 42)
        self.assertGreater(result.profile.instruction_count, 0)

    def test_rule_jump(self):
        code = ProgramCode(
            instructions=[
                Instruction("CONST", 0),
                Instruction("JUMP_IF_FALSE", 5),
                Instruction("CONST", 1),
                Instruction("STORE", 0),
                Instruction("JUMP", 7),
                Instruction("CONST", 2),
                Instruction("STORE", 0),
                Instruction("HALT"),
            ],
            constants=[True, 99, -1],
            names=["value"],
        )

        result = VirtualMachine().run(code)
        self.assertEqual(result.values["value"], 99)


if __name__ == "__main__":
    unittest.main()
