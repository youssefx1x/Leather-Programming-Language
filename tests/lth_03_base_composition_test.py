from src.lth03.base import BaseRegistry


registry = BaseRegistry()

registry.define(
    "Entity",
    {
        "active": True,
        "version": 1,
    },
)

registry.define(
    "Product",
    {
        "price": 100,
        "currency": "EGP",
    },
    extends="Entity",
)

registry.define(
    "VIPProduct",
    {
        "discount": 0.20,
    },
    extends="Product",
)

registry.validate()

item = registry.instantiate(
    "VIPProduct",
    {"price": 500},
)

assert item.base_name == "VIPProduct"
assert item["active"] is True
assert item["version"] == 1
assert item["price"] == 500
assert item["currency"] == "EGP"
assert item["discount"] == 0.20

print("LTH 0.3-F BASE COMPOSITION: PASS")
