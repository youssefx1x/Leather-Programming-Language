from __future__ import annotations

from dataclasses import dataclass

from .model import Instruction, ProgramCode


class CompilationError(Exception):
    pass


_MISSING = object()


def _first(node, *names, default=_MISSING):
    for name in names:
        if hasattr(node, name):
            value = getattr(node, name)
            if value is not None:
                return value
    if default is not _MISSING:
        return default
    raise CompilationError(
        f"AST node {type(node).__name__} is missing fields {names}"
    )


def _text(value):
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    for attr in ("value", "lexeme", "text", "name"):
        if hasattr(value, attr):
            nested = getattr(value, attr)
            if isinstance(nested, str):
                return nested
    return str(value)


def _kind(node):
    return type(node).__name__


def _sequence(value):
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return list(value)
    return [value]


def _program_body(node):
    return _sequence(
        _first(
            node,
            "statements",
            default=[],
        )
    )


class _Builder:
    def __init__(self):
        self.code = ProgramCode()
        self._constant_map = {}
        self._name_map = {}

    def const(self, value):
        try:
            hash(value)
            key = ("hashable", type(value), value)
        except TypeError:
            key = None

        if key is not None and key in self._constant_map:
            return self._constant_map[key]

        index = len(self.code.constants)
        self.code.constants.append(value)

        if key is not None:
            self._constant_map[key] = index

        return index

    def name(self, value):
        value = _text(value)
        if value not in self._name_map:
            self._name_map[value] = len(self.code.names)
            self.code.names.append(value)
        return self._name_map[value]

    def emit(self, op, arg=None, note=""):
        index = len(self.code.instructions)
        self.code.instructions.append(
            Instruction(op, arg, note)
        )
        return index

    def patch(self, index, arg):
        self.code.instructions[index].arg = arg


class LTH05Compiler:
    def compile_ast(self, program) -> ProgramCode:
        builder = _Builder()

        for statement in _program_body(program):
            self._compile_statement(builder, statement)

        builder.emit("HALT")
        return builder.code

    def compile_source(self, source: str) -> ProgramCode:
        program = self._parse_source(source)
        return self.compile_ast(program)

    def _parse_source(self, source):
        try:
            from src.lth03.lexer import Lexer
            from src.lth03.parser import Parser

            lexer = Lexer(source)

            if hasattr(lexer, "tokenize"):
                tokens = lexer.tokenize()
            elif hasattr(lexer, "lex"):
                tokens = lexer.lex()
            elif hasattr(lexer, "scan"):
                tokens = lexer.scan()
            else:
                raise CompilationError("LTH 0.3 lexer has no supported token method")

            parser = Parser(tokens)

            if hasattr(parser, "parse"):
                return parser.parse()
            if hasattr(parser, "parse_program"):
                return parser.parse_program()

            raise CompilationError("LTH 0.3 parser has no supported parse method")
        except CompilationError:
            raise
        except Exception as error:
            raise CompilationError(
                f"cannot parse LTH 0.5 source through 0.3 parser: {error}"
            ) from error

    def _compile_statement(self, builder, node):
        kind = _kind(node)

        if kind in {"Assignment", "Assign"}:
            self._compile_assignment(builder, node)
            return

        if kind in {"Rule", "ConditionalRule"}:
            self._compile_rule(builder, node)
            return

        if kind in {
            "Call",
            "Binary",
            "Unary",
            "Name",
            "Member",
            "Index",
            "Literal",
            "ListLiteral",
            "MapLiteral",
        }:
            self._compile_expression(builder, node)
            builder.emit("POP")
            return

        raise CompilationError(
            f"unsupported statement node: {kind}"
        )

    def _compile_rule(self, builder, node):
        condition = _first(
            node,
            "condition",
            "when",
            "test",
        )

        actions = _sequence(
            _first(
                node,
                "actions",
                "body",
                "effects",
                default=[],
            )
        )

        self._compile_expression(builder, condition)
        jump_end = builder.emit("JUMP_IF_FALSE", None)

        for action in actions:
            self._compile_statement(builder, action)

        builder.patch(
            jump_end,
            len(builder.code.instructions),
        )

    def _compile_assignment(self, builder, node):
        target = _first(node, "target", "name")
        target_kind = _kind(target)

        if target_kind not in {"Name", "Identifier"} and not isinstance(target, str):
            raise CompilationError(
                f"LTH 0.5 currently supports variable assignment targets only, "
                f"got {target_kind}"
            )

        name = _text(
            target if isinstance(target, str)
            else _first(target, "name", "identifier", "value")
        )

        operator = _text(
            _first(
                node,
                "operator",
                "op",
                default="=",
            )
        )

        if operator in {"", "="}:
            self._compile_expression(
                builder,
                _first(node, "expr"),
            )
        else:
            normalized = {
                "+=": "+",
                "-=": "-",
                "*=": "*",
                "/=": "/",
                "//=": "//",
                "%=": "%",
                "**=": "**",
            }.get(operator)

            if normalized is None:
                raise CompilationError(
                    f"unsupported assignment operator: {operator}"
                )

            builder.emit(
                "LOAD",
                builder.name(name),
                f"load {name}",
            )

            self._compile_expression(
                builder,
                _first(node, "expr"),
            )

            builder.emit("BINARY", normalized)

        builder.emit(
            "STORE",
            builder.name(name),
            f"store {name}",
        )

    def _compile_expression(self, builder, node):
        kind = _kind(node)

        if kind in {"Literal", "Value"}:
            value = _first(
                node,
                "value",
                "literal",
                "data",
            )
            builder.emit(
                "CONST",
                builder.const(value),
            )
            return

        if kind in {"Name", "Identifier"}:
            name = _text(
                _first(node, "name", "identifier", "value")
            )
            builder.emit(
                "LOAD",
                builder.name(name),
                f"load {name}",
            )
            return

        if kind == "ListLiteral":
            items = _sequence(
                _first(
                    node,
                    "items",
                    "elements",
                    "values",
                    default=[],
                )
            )
            for item in items:
                self._compile_expression(builder, item)
            builder.emit("BUILD_LIST", len(items))
            return

        if kind == "MapLiteral":
            entries = _first(
                node,
                "entries",
                "items",
                "pairs",
                "values",
                default=[],
            )

            if isinstance(entries, dict):
                entries = list(entries.items())

            for entry in entries:
                if isinstance(entry, tuple) and len(entry) == 2:
                    key, value = entry
                else:
                    key = _first(entry, "key", "name")
                    value = _first(entry, "value", "expression")

                if isinstance(key, str):
                    builder.emit(
                        "CONST",
                        builder.const(key),
                    )
                else:
                    self._compile_expression(builder, key)

                self._compile_expression(builder, value)

            builder.emit("BUILD_MAP", len(entries))
            return

        if kind == "Member":
            obj = _first(
                node,
                "object",
                "obj",
                "value",
            )
            member = _first(
                node,
                "name",
                "member",
                "attribute",
            )
            self._compile_expression(builder, obj)
            builder.emit(
                "LOAD_MEMBER",
                _text(member),
            )
            return

        if kind == "Index":
            obj = _first(
                node,
                "object",
                "obj",
                "value",
            )
            index = _first(node, "index", "key")
            self._compile_expression(builder, obj)
            self._compile_expression(builder, index)
            builder.emit("LOAD_INDEX")
            return

        if kind == "Unary":
            operator = _text(
                _first(node, "operator", "op")
            )
            operand = _first(
                node,
                "operand",
                "value",
                "expression",
            )
            self._compile_expression(builder, operand)
            builder.emit("UNARY", operator)
            return

        if kind == "Binary":
            left = _first(
                node,
                "left",
                "lhs",
            )
            right = _first(
                node,
                "right",
                "rhs",
            )
            operator = _text(
                _first(node, "operator", "op")
            )

            self._compile_expression(builder, left)
            self._compile_expression(builder, right)
            builder.emit("BINARY", operator)
            return

        if kind == "Call":
            callee = _first(
                node,
                "name",
                "callee",
                "function",
                "func",
                "target",
            )
            args = _sequence(
                _first(
                    node,
                    "args",
                    "arguments",
                    "parameters",
                    default=[],
                )
            )

            if isinstance(callee, str):
                builder.emit(
                    "LOAD",
                    builder.name(callee),
                    f"load {callee}",
                )
            else:
                self._compile_expression(builder, callee)

            for arg in args:
                self._compile_expression(builder, arg)

            builder.emit("CALL", len(args))
            return

        raise CompilationError(
            f"unsupported expression node: {kind}"
        )
