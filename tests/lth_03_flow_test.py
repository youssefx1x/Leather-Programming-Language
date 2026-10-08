from src.lth03.final_runner import LTH03FinalRunner


source = """
flow subtotal {
    total = price * quantity
}

run flow subtotal
"""

state = LTH03FinalRunner().run(
    source,
    context={
        "price": 10,
        "quantity": 3,
    },
)

assert state.values["total"] == 30

print("LTH 0.3-G FLOW: PASS")
