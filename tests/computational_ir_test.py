from src.semantic.computational_model import (
    Domain,
    State,
    StateField,
    Operation,
    OperationInput,
    Transition,
)
from src.semantic.unified_model import UnifiedSemanticProgram
from src.ir.computational_compiler import ComputationalIRCompiler


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

    ir = ComputationalIRCompiler().compile(program)

    actual = [
        instruction.opcode
        for instruction in ir.instructions
    ]

    expected = [
        "DOMAIN_BEGIN",
        "DOMAIN_END",

        "STATE_BEGIN",
        "STATE_FIELD",
        "STATE_FIELD",
        "STATE_END",

        "OPERATION_BEGIN",
        "OPERATION_INPUT",
        "OPERATION_INPUT",
        "OPERATION_END",

        "TRANSITION",
    ]

    assert actual == expected

    transition_instruction = ir.instructions[-1]

    assert transition_instruction.operands == (
        "position",
        "move",
        "position",
    )

    print("CORE 0.2 COMPUTATIONAL IR: PASS")
    print(ir.describe())


if __name__ == "__main__":
    main()
