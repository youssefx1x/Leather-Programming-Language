from src.lth03 import LTH03Runner


def main():
    source = """
items = [10, 20, 30]
user = {
    name: "VIP",
    score: 95
}
first = items[0]
username = user.name
count = len(items)
"""

    values = LTH03Runner().run(source).values

    assert values["items"] == [10, 20, 30]
    assert values["first"] == 10
    assert values["username"] == "VIP"
    assert values["count"] == 3
    assert values["user"]["score"] == 95

    print("LTH 0.3 COLLECTIONS TEST: PASS")


if __name__ == "__main__":
    main()
