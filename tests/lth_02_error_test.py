from tools.errors import (
    LeatherError,
    LeatherLexError,
    LeatherSemanticError,
    LeatherIRError,
    LeatherRuntimeError,
    LeatherInputError,
)


def test_base_error():
    error = LeatherError("something went wrong")

    assert error.format() == (
        "LTH Error [error]: something went wrong"
    )


def test_lexer_error():
    error = LeatherLexError(
        "unexpected character '@'",
        line=3,
        column=7,
    )

    assert error.format() == (
        "LTH Error [lexer] at 3:7: "
        "unexpected character '@'"
    )


def test_semantic_error():
    error = LeatherSemanticError(
        "unknown value 'price'",
    )

    assert error.format() == (
        "LTH Error [semantic]: "
        "unknown value 'price'"
    )


def test_ir_error():
    error = LeatherIRError(
        "unknown opcode 'BAD'",
    )

    assert error.format() == (
        "LTH Error [ir]: unknown opcode 'BAD'"
    )


def test_runtime_error():
    error = LeatherRuntimeError(
        "unknown runtime value 'price'",
    )

    assert error.format() == (
        "LTH Error [runtime]: "
        "unknown runtime value 'price'"
    )


def test_input_error():
    error = LeatherInputError(
        "context root must be a JSON object",
    )

    assert error.format() == (
        "LTH Error [input]: "
        "context root must be a JSON object"
    )


if __name__ == "__main__":
    test_base_error()
    test_lexer_error()
    test_semantic_error()
    test_ir_error()
    test_runtime_error()
    test_input_error()

    print("LTH 0.2 ERROR TEST: PASS")
