from src.lth04.equivalence import equivalent


source = """
price = 150
quantity = 3
rule discount when customer.vip -> price *= 0.90
total = price * quantity
"""

assert equivalent(
    source,
    context={
        "customer": {
            "vip": True,
        },
    },
)

assert equivalent(
    source,
    context={
        "customer": {
            "vip": False,
        },
    },
)

print("LTH 0.4 SEMANTIC EQUIVALENCE: PASS")
