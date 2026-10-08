import unittest

from src.lth05.compiler import LTH05Compiler
from src.lth05.optimizer import optimize


class LTH05OptimizerTest(unittest.TestCase):
    def test_constant_folding(self):
        source = "value = 2 + 3 * 4"

        code = LTH05Compiler().compile_source(source)
        optimized, report = optimize(code)

        self.assertGreaterEqual(
            report["constant_folds"],
            1,
        )

        ops = [item.op for item in optimized.instructions]

        self.assertIn("CONST", ops)
        self.assertIn("HALT", ops)


if __name__ == "__main__":
    unittest.main()
