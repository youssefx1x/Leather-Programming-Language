from src.lth04.runner import LTH04Runner


source = """
price = 100
quantity = 4
total = price * quantity
"""

runner = LTH04Runner()

state = runner.run(source)

assert state.values["price"] == 100
assert state.values["quantity"] == 4
assert state.values["total"] == 400

print("LTH 0.4 VM: PASS")
