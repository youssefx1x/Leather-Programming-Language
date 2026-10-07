from dataclasses import dataclass


@dataclass(frozen=True)
class WorkUnit:
    identifier: int
    payload: object


@dataclass(frozen=True)
class ExecutionBatch:
    index: int
    units: tuple

    @property
    def size(self):
        return len(self.units)


class ExecutionScheduler:
    def partition(self, items, batch_size=1):
        if batch_size < 1:
            raise ValueError(
                "batch_size must be >= 1"
            )

        units = tuple(
            WorkUnit(
                identifier=index,
                payload=value,
            )
            for index, value in enumerate(items)
        )

        batches = []

        for start in range(
            0,
            len(units),
            batch_size,
        ):
            batches.append(
                ExecutionBatch(
                    index=len(batches),
                    units=units[
                        start:start + batch_size
                    ],
                )
            )

        return tuple(batches)

    def flatten(self, batches):
        result = []

        for batch in batches:
            result.extend(
                unit.payload
                for unit in batch.units
            )

        return tuple(result)
