from src.lth03.base import BaseError, BaseRegistry


registry = BaseRegistry()

try:
    registry.get("Missing")
except BaseError:
    pass
else:
    raise AssertionError("unknown base must fail")

registry.define("A", {"x": 1})

try:
    registry.define("A", {"x": 2})
except BaseError:
    pass
else:
    raise AssertionError("duplicate base must fail")

try:
    registry.get("B")
except BaseError:
    pass
else:
    raise AssertionError("unknown base must fail")

print("LTH 0.3-F BASE VALIDATION: PASS")
