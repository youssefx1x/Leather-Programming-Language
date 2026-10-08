import unittest

from src.lth05.model import Instruction, ProgramCode


class LTH05BytecodeTest(unittest.TestCase):
    def test_instruction_model(self):
        code = ProgramCode(
            instructions=[
                Instruction("CONST", 0),
                Instruction("HALT"),
            ],
            constants=[42],
            names=[],
        )

        self.assertEqual(len(code.instructions), 2)
        self.assertEqual(code.constants[0], 42)
        self.assertIn("0000 CONST", code.disassemble())
        self.assertIn("0001 HALT", code.disassemble())


if __name__ == "__main__":
    unittest.main()
