from src.lth03 import LTH03Runner


def main():
    source = """
price = 150.5
quantity = 2
total = price * quantity
score = (10 + 5) * 2
ratio = 100 / 4
remainder = 17 % 5
"""

    values = LTH03Runner().run(source).values

    assert values["total"] == 301.0
    assert values["score"] == 30
    assert values["ratio"] == 25
    assert values["remainder"] == 2

    print("LTH 0.3 EXPRESSION TEST: PASS")


if __name__ == "__main__":
    main()
