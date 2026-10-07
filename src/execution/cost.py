from src.execution.measurement import ExecutionMeasurement
from src.optimizer.performance_model import PerformanceCost


def observed_cost(measurement):
    return PerformanceCost(
        time=float(max(1, measurement.operations)),
        memory=float(max(1, measurement.states)),
        states=float(max(1, measurement.states)),
        branching=float(max(1, measurement.branches)),
        depth=1.0,
        precision=1.0,
        interactions=float(
            max(
                1,
                measurement.branches,
            )
        ),
    )


def wall_clock_cost(measurement):
    return PerformanceCost(
        time=float(max(1, measurement.elapsed_ns)),
        memory=float(max(1, measurement.states)),
        states=float(max(1, measurement.states)),
        branching=float(max(1, measurement.branches)),
        depth=1.0,
        precision=1.0,
        interactions=float(
            max(
                1,
                measurement.branches,
            )
        ),
    )
