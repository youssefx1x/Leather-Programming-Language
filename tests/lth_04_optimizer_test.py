from src.lth04.model import BytecodeProgram, Instruction
from src.lth04.optimizer import BytecodeOptimizer


program = BytecodeProgram(
    instructions=(
        Instruction("NOP"),
        Instruction("EXECUTE", "x = 1"),
        Instruction("NOP"),
        Instruction("HALT"),
        Instruction("EXECUTE", "x = 999"),
    ),
    source_hash="x",
    prepared_source="x = 1",
    statement_count=1,
)

optimizer = BytecodeOptimizer()

optimized = optimizer.optimize(program)

assert [i.op for i in optimized.instructions] == [
    "EXECUTE",
    "HALT",
]

assert optimized.optimized is True
assert optimizer.validate(optimized) is True

print("LTH 0.4 OPTIMIZER: PASS")
