from src.lth04.runner import LTH04Runner


source = """
price = 80
quantity = 2
total = price * quantity
"""

runner = LTH04Runner(
    use_cache=True
)

runner.run(source)

assert runner.cache.misses == 1
assert runner.cache.hits == 0
assert len(runner.cache) == 1

runner.run(source)

assert runner.cache.hits == 1
assert len(runner.cache) == 1

print("LTH 0.4 CACHE: PASS")
