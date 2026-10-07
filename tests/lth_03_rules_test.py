from src.lth03 import LTH03Runner


def main():
    source = """
price = 150.5
priority = false

rule vip when customer.vip and cart.total > 100 -> price *= 0.9; priority = true
"""

    context = {
        "customer": {
            "vip": True,
        },
        "cart": {
            "total": 120,
        },
    }

    values = LTH03Runner().run(
        source,
        context=context,
    ).values

    assert abs(values["price"] - 135.45) < 1e-9
    assert values["priority"] is True

    print("LTH 0.3 RULES 2.0 TEST: PASS")


if __name__ == "__main__":
    main()
