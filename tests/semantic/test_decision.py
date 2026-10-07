from src.semantic.intent import Intent, SlotState
from src.semantic.decision import DecisionEngine


intent = Intent()

intent.define(
    "execution.mode",
    SlotState.AUTO,
)

intent.define(
    "memory.strategy",
    SlotState.FIXED,
    "streaming",
)

intent.define(
    "compression.algorithm",
    SlotState.OPEN,
)

engine = DecisionEngine()

auto_decision = engine.decide(
    intent.get("execution.mode"),
    {"memory_mb": 512},
)

fixed_decision = engine.decide(
    intent.get("memory.strategy"),
)

open_decision = engine.decide(
    intent.get("compression.algorithm"),
)

print("AUTO:")
print(auto_decision)

print("FIXED:")
print(fixed_decision)

print("OPEN:")
print(open_decision)
