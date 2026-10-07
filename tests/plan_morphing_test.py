from src.runtime.observation import RuntimeObservation
from src.runtime.morphing import PlanMorpher


def test_plan_morphing():
    morpher = PlanMorpher()

    observation = RuntimeObservation(
        memory_mb=128,
    )

    decision = morpher.decide(
        target="backup",
        current_strategy="latency",
        observation=observation,
    )

    assert decision is not None
    assert decision.target == "backup"
    assert decision.old_strategy == "latency"
    assert decision.new_strategy == "streaming"

    print("MORPH DECISION:")
    print(decision)

    print("PLAN MORPHING TEST PASSED")


if __name__ == "__main__":
    test_plan_morphing()
