from src.execution.memo import ExecutionMemo


def fibonacci_direct(n, counter):
    counter.state()

    if n <= 1:
        counter.operation()
        return n

    counter.branch(2)
    counter.operation()

    return (
        fibonacci_direct(n - 1, counter)
        + fibonacci_direct(n - 2, counter)
    )


def fibonacci_memoized(n, counter, memo=None):
    if memo is None:
        memo = ExecutionMemo()

    counter.state()

    if memo.contains(n):
        counter.hit()
        return memo.get(n)

    counter.miss()

    if n <= 1:
        counter.operation()
        result = n
    else:
        counter.branch(2)
        counter.operation()
        result = (
            fibonacci_memoized(n - 1, counter, memo)
            + fibonacci_memoized(n - 2, counter, memo)
        )

    memo.set(n, result)
    return result
