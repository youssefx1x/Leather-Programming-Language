from dataclasses import dataclass


@dataclass(frozen=True)
class ResourceEnvelope:
    """
    Execution constraints available to the semantic planner.

    None means that the resource is unconstrained.
    """

    memory_mb: int | None = None
    time_ms: int | None = None
    cpu: int | None = None
    gpu: int | None = None
    network: bool | None = None
    energy: str | None = None

    def describe(self):
        values = []

        if self.memory_mb is not None:
            values.append(f"memory={self.memory_mb}MB")

        if self.time_ms is not None:
            values.append(f"time={self.time_ms}ms")

        if self.cpu is not None:
            values.append(f"cpu={self.cpu}")

        if self.gpu is not None:
            values.append(f"gpu={self.gpu}")

        if self.network is not None:
            values.append(f"network={self.network}")

        if self.energy is not None:
            values.append(f"energy={self.energy}")

        return "RESOURCE ENVELOPE: " + (
            ", ".join(values) if values else "unconstrained"
        )
