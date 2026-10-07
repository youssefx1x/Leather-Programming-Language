from src.runtime.evidence import ExecutionEvidence
from src.runtime.trace import ExecutionTrace


trace = ExecutionTrace()

trace.record(
    "CHECK",
    "customer.vip = true",
)

trace.record(
    "ACTIVATE",
    "rule discount activated",
)

trace.record(
    "CHANGE",
    "price: 150.5 -> 135.45",
)

evidence = ExecutionEvidence(trace)

activation = evidence.why_rule_activated(
    "discount"
)

if activation != "rule discount activated":
    print("TEST FAILED: activation evidence missing")
    raise SystemExit(1)

changes = evidence.changes("price")

if len(changes) != 1:
    print("TEST FAILED: change evidence missing")
    raise SystemExit(1)

print(evidence.describe())
print()
print("WHY:")
print(activation)
print()
print("EVIDENCE TEST PASSED")
