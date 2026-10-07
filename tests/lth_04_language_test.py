from src.lth04.runner import LTH04Runner


source = """
base Product {
    price = 100
    active = true
}

flow subtotal {
    total = item.price * quantity
}

flow discount {
    total = total * 0.90
}

system Shop {
    use flow subtotal
    use flow discount
}

item = Product({"price": 250})
run system Shop
"""

state = LTH04Runner().run(
    source,
    context={
        "quantity": 2,
    },
)

assert state.values["item"]["price"] == 250
assert state.values["total"] == 450.0

print("LTH 0.4 FULL LANGUAGE: PASS")
