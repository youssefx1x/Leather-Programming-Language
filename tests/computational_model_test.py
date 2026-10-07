from src.semantic.computational_model import (
    Domain,
    State,
    StateField,
    Operation,
    OperationInput,
    Transition,
)


def main():
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

    assert chess.name == "chess"

    assert len(chess.states) == 1
    assert chess.states[0].name == "position"
    assert len(chess.states[0].fields) == 2

    assert chess.states[0].fields[0].name == "board"
    assert chess.states[0].fields[0].semantic_type == "board"

    assert len(chess.operations) == 1
    assert chess.operations[0].name == "move"
    assert len(chess.operations[0].inputs) == 2

    assert chess.operations[0].inputs[0].name == "from"
    assert chess.operations[0].inputs[0].semantic_type == "square"

    assert len(chess.transitions) == 1

    transition = chess.transitions[0]

    assert transition.source_state == "position"
    assert transition.operation == "move"
    assert transition.target_state == "position"

    print("CORE 0.2 COMPUTATIONAL MODEL: PASS")


if __name__ == "__main__":
    main()
