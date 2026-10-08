from src.lth03.base_runner import BaseAwareRunner


source = """
base Product {
    price = 100
    active = true
}

base VIPProduct extends Product {
    discount = 0.20
}

item = VIPProduct({"price": 250})
price = item.price
discount = item.discount
active = item.active
"""

result = BaseAwareRunner().run(source).values

assert result["item"]["price"] == 250
assert result["item"]["active"] is True
assert result["item"]["discount"] == 0.20
assert result["price"] == 250
assert result["discount"] == 0.20
assert result["active"] is True

print("LTH 0.3-F BASE LANGUAGE: PASS")
