from src.lth03 import LTH03Runner


def main():
    source = """
name = "Leather"
age = 20
active = true
missing = null
"""

    values = LTH03Runner().run(source).values

    assert values["name"] == "Leather"
    assert values["age"] == 20
    assert values["active"] is True
    assert values["missing"] is None

    print("LTH 0.3 VALUES TEST: PASS")


if __name__ == "__main__":
    main()
