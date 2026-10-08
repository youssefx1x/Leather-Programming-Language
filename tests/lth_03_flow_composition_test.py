from src.lth03.final_runner import LTH03FinalRunner


source = """
flow subtotal {
    total = price * quantity
}

flow discount {
    total = total * 0.90
}

system Shop {
    use flow subtotal
    use flow discount
}

run system Shop
"""

state = LTH03FinalRunner().run(
    source,
    context={
        "price": 100,
        "quantity": 2,
    },
)

assert state.values["total"] == 180.0

print("LTH 0.3-G FLOW COMPOSITION: PASS")
