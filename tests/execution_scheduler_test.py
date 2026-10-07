from src.execution.scheduler import (
    ExecutionScheduler,
)


def main():
    scheduler = ExecutionScheduler()

    batches = scheduler.partition(
        range(10),
        batch_size=3,
    )

    assert len(batches) == 4
    assert batches[0].size == 3
    assert batches[-1].size == 1

    flattened = scheduler.flatten(
        batches
    )

    assert flattened == tuple(range(10))

    print("LTH EXECUTION SCHEDULER: PASS")


if __name__ == "__main__":
    main()
