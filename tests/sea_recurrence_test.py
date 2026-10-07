from src.sea_recurrence import (
    fibonacci_recurrence,
    binary_tree_recurrence,
)


def main():
    fib = fibonacci_recurrence()

    assert fib.evaluate(0) == 0
    assert fib.evaluate(1) == 1
    assert fib.evaluate(10) == 55
    assert fib.evaluate(20) == 6765

    tree = binary_tree_recurrence()

    assert tree.evaluate(0) == 1
    assert tree.evaluate(1) == 3
    assert tree.evaluate(4) == 31

    print("SEA 0.4 RECURRENCE ALGEBRA: PASS")


if __name__ == "__main__":
    main()
