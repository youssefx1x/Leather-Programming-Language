from src.lth04.benchmark import benchmark


source = """
x = 2
y = 4
z = x * y
"""

result = benchmark(
    source,
    iterations=3,
)

assert result["iterations"] == 3
assert result["reference_total"] >= 0
assert result["accelerated_total"] >= 0
assert result["reference_avg"] >= 0
assert result["accelerated_avg"] >= 0
assert result["speedup_ratio"] >= 0

print("LTH 0.4 BENCHMARK: PASS")
print(
    "LTH 0.4 SPEEDUP RATIO:",
    result["speedup_ratio"],
)
