from src.semantic.resource_envelope import ResourceEnvelope
from src.semantic.resource_intent import ResourceIntentResolver


def test_low_memory():
    envelope = ResourceEnvelope(
        memory_mb=256,
    )

    intent = ResourceIntentResolver().resolve(envelope)

    decision = intent.get_decision(
        "memory.strategy"
    )

    assert decision["value"] == "streaming"


def test_moderate_memory():
    envelope = ResourceEnvelope(
        memory_mb=768,
    )

    intent = ResourceIntentResolver().resolve(envelope)

    decision = intent.get_decision(
        "memory.strategy"
    )

    assert decision["value"] == "bounded"


def test_large_memory():
    envelope = ResourceEnvelope(
        memory_mb=4096,
    )

    intent = ResourceIntentResolver().resolve(envelope)

    decision = intent.get_decision(
        "memory.strategy"
    )

    assert decision["value"] == "adaptive"


def test_tight_time():
    envelope = ResourceEnvelope(
        time_ms=500,
    )

    intent = ResourceIntentResolver().resolve(envelope)

    decision = intent.get_decision(
        "execution.mode"
    )

    assert decision["value"] == "latency"


def test_gpu():
    envelope = ResourceEnvelope(
        gpu=1,
    )

    intent = ResourceIntentResolver().resolve(envelope)

    decision = intent.get_decision(
        "compute.target"
    )

    assert decision["value"] == "gpu"


def test_combined_constraints():
    envelope = ResourceEnvelope(
        memory_mb=256,
        time_ms=500,
        cpu=4,
        gpu=1,
    )

    intent = ResourceIntentResolver().resolve(envelope)

    assert intent.get_decision(
        "memory.strategy"
    )["value"] == "streaming"

    assert intent.get_decision(
        "execution.mode"
    )["value"] == "latency"

    assert intent.get_decision(
        "compute.target"
    )["value"] == "gpu"


if __name__ == "__main__":
    test_low_memory()
    test_moderate_memory()
    test_large_memory()
    test_tight_time()
    test_gpu()
    test_combined_constraints()

    print("RESOURCE ENVELOPE TEST PASSED")
