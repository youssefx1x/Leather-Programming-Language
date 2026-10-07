from src.lth04.compiler import BytecodeCompiler


source = """
price = 100
quantity = 3
total = price * quantity
"""

program = BytecodeCompiler().compile(source)

assert len(program.instructions) == 2
assert program.instructions[0].op == "EXECUTE"
assert program.instructions[1].op == "HALT"
assert len(program.source_hash) == 64
assert program.statement_count == 3

print("LTH 0.4 COMPILE: PASS")
