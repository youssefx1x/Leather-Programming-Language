from src.lth03.base import BaseRegistry


registry = BaseRegistry()

registry.define(
    "Product",
    {
        "price": 100,
        "active": True,
    },
)

registry.define(
    "VIPProduct",
    {
        "discount": 0.20,
    },
    extends="Product",
)

result = registry.instantiate("VIPProduct")

assert result == {
    "price": 100,
    "active": True,
    "discount": 0.20,
}

result = registry.instantiate(
    "VIPProduct",
    {"price": 200},
)

assert result["price"] == 200
assert result["active"] is True
assert result["discount"] == 0.20

print("LTH 0.3-F BASE EXTENSION: PASS")
