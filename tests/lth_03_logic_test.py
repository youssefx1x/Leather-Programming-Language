from src.lth03 import LTH03Runner


def main():
    source = """
adult = age >= 18
good = score > 80 and active
blocked = not active
either = score > 100 or active
"""

    context = {
        "age": 20,
        "score": 95,
        "active": True,
    }

    values = LTH03Runner().run(
        source,
        context=context,
    ).values

    assert values["adult"] is True
    assert values["good"] is True
    assert values["blocked"] is False
    assert values["either"] is True

    print("LTH 0.3 LOGIC TEST: PASS")


if __name__ == "__main__":
    main()
