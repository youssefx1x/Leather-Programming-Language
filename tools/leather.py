import argparse
import json
import sys
from pathlib import Path

from src.lexer.lexer import Lexer, LexerError
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer
from src.semantic.builder import SemanticBuilder
from src.semantic.planner import SemanticPlanner
from src.ir.compiler import IRCompiler
from src.ir.validator import IRValidator
from src.runtime.explainable import ExplainableRuntime
from src.runtime.runtime import RuntimeErrorLTH

from tools.errors import (
    LeatherError,
    LeatherInputError,
    LeatherIRError,
    LeatherLexError,
    LeatherParseError,
    LeatherRuntimeError,
    LeatherSemanticError,
)


def compile_source(source):
    try:
        tokens = Lexer(source).tokenize()
    except LexerError:
        raise

    try:
        program = Parser(tokens).parse()
    except SyntaxError as error:
        raise LeatherParseError(
            str(error),
        ) from error

    analyzer = SemanticAnalyzer()
    errors = analyzer.analyze(program)

    if errors:
        messages = "\n".join(
            f"  - {error.message}"
            for error in errors
        )

        raise LeatherSemanticError(
            messages,
        )

    semantic_program = SemanticBuilder().build(
        program
    )

    plan = SemanticPlanner().plan(
        semantic_program
    )

    ir = IRCompiler().compile(
        semantic_program
    )

    validation_errors = IRValidator().validate(ir)

    if validation_errors:
        messages = "\n".join(
            f"  - [{error.index}] {error.message}"
            for error in validation_errors
        )

        raise LeatherIRError(
            messages,
        )

    return semantic_program, plan, ir


def load_context(path):
    if path is None:
        return {}

    if not path.exists():
        raise LeatherInputError(
            f"context file not found: {path}"
        )

    if not path.is_file():
        raise LeatherInputError(
            f"context path is not a file: {path}"
        )

    try:
        with path.open(
            "r",
            encoding="utf-8",
        ) as context_file:
            context = json.load(context_file)
    except json.JSONDecodeError as error:
        raise LeatherInputError(
            f"invalid JSON context: {error.msg}"
        ) from error
    except OSError as error:
        raise LeatherInputError(
            f"cannot read context file: {error}"
        ) from error

    if not isinstance(context, dict):
        raise LeatherInputError(
            "context root must be a JSON object"
        )

    return context


def execute_file(
    path,
    show_plan=False,
    show_ir=False,
    context=None,
):
    try:
        source = path.read_text(
            encoding="utf-8"
        )
    except OSError as error:
        raise LeatherInputError(
            f"cannot read source file: {error}"
        ) from error

    semantic_program, plan, ir = compile_source(
        source
    )

    if show_plan:
        print(plan.describe())
        print()

    if show_ir:
        print(ir.describe())
        print()

    runtime = ExplainableRuntime()

    try:
        state = runtime.execute(
            ir,
            context=context or {},
        )
    except (
        RuntimeErrorLTH,
        TypeError,
        ValueError,
        OverflowError,
    ) as error:
        raise LeatherRuntimeError(
            str(error)
        ) from error

    print("LTH RESULT")

    for name, value in state.values.items():
        print(f"  {name} = {value}")

    print()
    print("LTH TRACE")
    print(runtime.trace.describe())

    return state


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="leather",
        description="Leather Programming Language runner",
    )

    parser.add_argument(
        "file",
        type=Path,
        help="LTH source file",
    )

    parser.add_argument(
        "--plan",
        action="store_true",
        help="show the semantic execution plan",
    )

    parser.add_argument(
        "--ir",
        action="store_true",
        help="show generated LTH IR",
    )

    parser.add_argument(
        "--context",
        type=Path,
        help="JSON runtime context file",
    )

    args = parser.parse_args(argv)

    if not args.file.exists():
        error = LeatherInputError(
            f"file not found: {args.file}"
        )
        print(
            error.format(),
            file=sys.stderr,
        )
        return 2

    if not args.file.is_file():
        error = LeatherInputError(
            f"not a file: {args.file}"
        )
        print(
            error.format(),
            file=sys.stderr,
        )
        return 2

    try:
        context = load_context(
            args.context
        )

        execute_file(
            args.file,
            show_plan=args.plan,
            show_ir=args.ir,
            context=context,
        )

    except LexerError as error:
        formatted = LeatherLexError(
            error.args[0],
            line=error.line,
            column=error.column,
        )
        print(
            formatted.format(),
            file=sys.stderr,
        )
        return 1

    except LeatherError as error:
        print(
            error.format(),
            file=sys.stderr,
        )
        return 1

    except SyntaxError as error:
        formatted = LeatherParseError(
            str(error),
        )
        print(
            formatted.format(),
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
