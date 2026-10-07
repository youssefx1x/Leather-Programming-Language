from src.lth03 import LTH03Runner


def main():
    source = """
name = "Leather"
price = 150.5
quantity = 2
items = [10, 20, 30]

user = {
    vip: true,
    name: "VIP"
}

active = true

total = price * quantity
large_order = total > 250

rule discount when user.vip and active and quantity > 1 -> price *= 0.9; quantity += 1
"""

    values = LTH03Runner().run(source).values

    assert values["name"] == "Leather"
    assert abs(values["total"] - 301.0) < 1e-9
    assert values["large_order"] is True
    assert abs(values["price"] - 135.45) < 1e-9
    assert values["quantity"] == 3
    assert values["user"]["vip"] is True
    assert values["items"] == [10, 20, 30]

    print("LTH 0.3 FULL 50% INTEGRATION TEST: PASS")


if __name__ == "__main__":
    main()
