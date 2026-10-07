from src.lth04.runner import LTH04Runner


source = """
x = 2
y = x * 5
"""

runner = LTH04Runner()

state, stats = runner.execute(
    source,
    trace=True,
)

assert state.values["y"] == 10
assert stats.instruction_count == 2
assert len(stats.trace) == 2
assert stats.trace[0]["op"] == "EXECUTE"
assert stats.trace[1]["op"] == "HALT"

print("LTH 0.4 TRACE: PASS")
