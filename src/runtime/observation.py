from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimeObservation:
    elapsed_ms: float | None = None
    memory_mb: int | None = None
    cpu_load: float | None = None
    throughput: float | None = None

    def describe(self):
        values = []

        if self.elapsed_ms is not None:
            values.append(f"elapsed={self.elapsed_ms}ms")

        if self.memory_mb is not None:
            values.append(f"memory={self.memory_mb}MB")

        if self.cpu_load is not None:
            values.append(f"cpu_load={self.cpu_load}")

        if self.throughput is not None:
            values.append(f"throughput={self.throughput}")

        return "OBSERVATION: " + (
            ", ".join(values) if values else "empty"
        )
