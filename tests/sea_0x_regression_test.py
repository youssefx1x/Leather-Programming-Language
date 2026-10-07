from src.sea_04 import build_demo_report


def main():
    report = build_demo_report()

    assert report.valid

    print("SEA 0.X GLOBAL REGRESSION: PASS")


if __name__ == "__main__":
    main()
