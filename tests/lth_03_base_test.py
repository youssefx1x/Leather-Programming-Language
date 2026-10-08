from src.lth03.base import BaseError, BaseRegistry


registry = BaseRegistry()

product = registry.define(
    "Product",
    {
        "price": 100,
        "active": True,
    },
)

assert product.instantiate() == {
    "price": 100,
    "active": True,
}

assert registry.instantiate(
    "Product",
    {"price": 150},
) == {
    "price": 150,
    "active": True,
}

try:
    registry.define("Product", {})
except BaseError:
    pass
else:
    raise AssertionError("duplicate base must fail")

print("LTH 0.3-F BASE: PASS")
