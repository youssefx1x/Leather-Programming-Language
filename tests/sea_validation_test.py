from src.sea_recurrence import fibonacci_recurrence
from src.sea_validation import validate_recurrence


def main():
    report = validate_recurrence(
        fibonacci_recurrence()
    )

    assert report.valid
    assert report.count == 0

    print("SEA 0.4 VALIDATION LAYER: PASS")


if __name__ == "__main__":
    main()
