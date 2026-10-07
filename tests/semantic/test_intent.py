from src.semantic.intent import Intent, SlotState


intent = Intent()

intent.define(
    "compression.algorithm",
    SlotState.AUTO,
)

intent.define(
    "execution.mode",
    SlotState.OPEN,
)

intent.define(
    "memory.strategy",
    SlotState.FIXED,
    "streaming",
)

print(intent.describe())
