from src.runtime.trace import ExecutionTrace


trace = ExecutionTrace()

trace.record(
    "DEFINE",
    "price = 150.5",
)

trace.record(
    "CHECK",
    "customer.vip = true",
)

trace.record(
    "ACTIVATE",
    "rule discount activated",
)

trace.record(
    "EFFECT",
    "price *= 0.9",
)

trace.record(
    "CHANGE",
    "price: 150.5 -> 135.45",
)

print(trace.describe())
