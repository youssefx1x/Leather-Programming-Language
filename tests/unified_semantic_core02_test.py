from src.semantic.unified_model import UnifiedSemanticProgram
from src.semantic.computational_model import (
    Domain,
    State,
    StateField,
    Operation,
    OperationInput,
    Transition,
)


def main():
    program = UnifiedSemanticProgram()

    position = State(
        name="position",
        domain="chess",
        fields=(
            StateField("board", "board"),
            StateField("side", "side"),
        ),
    )

    move = Operation(
        name="move",
        inputs=(
            OperationInput("from", "square"),
            OperationInput("to", "square"),
        ),
    )

    transition = Transition(
        source_state="position",
        operation="move",
        target_state="position",
    )

    chess = Domain(
        name="chess",
        states=(position,),
        operations=(move,),
        transitions=(transition,),
    )

    program.domains.append(chess)
    program.states.append(position)
    program.operations.append(move)
    program.transitions.append(transition)

    counts = program.counts()

    assert counts["domains"] == 1
    assert counts["states"] == 1
    assert counts["operations"] == 1
    assert counts["transitions"] == 1

    assert len(program.all_items()) == 4

    print("UNIFIED CORE 0.2 SEMANTIC MODEL: PASS")
    print(counts)


if __name__ == "__main__":
    main()
