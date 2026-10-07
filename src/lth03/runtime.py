from dataclasses import dataclass


class LTH03RuntimeError(Exception):
    pass


@dataclass
class State:
    values: dict
    context: dict


class Evaluator:
    def __init__(self, context=None):
        self.state = State(
            values={},
            context=context or {},
        )

    def get_name(self, name):
        if name in self.state.values:
            return self.state.values[name]

        if name in self.state.context:
            return self.state.context[name]

        raise LTH03RuntimeError(
            f"unknown value '{name}'"
        )

    def eval(self, node):
        from .ast import (
            Binary,
            Call,
            Index,
            ListLiteral,
            Literal,
            MapLiteral,
            Member,
            Name,
            Unary,
        )

        if isinstance(node, Literal):
            return node.value

        if isinstance(node, ListLiteral):
            return [
                self.eval(item)
                for item in node.items
            ]

        if isinstance(node, MapLiteral):
            return {
                key: self.eval(value)
                for key, value in node.items
            }

        if isinstance(node, Name):
            return self.get_name(node.name)

        if isinstance(node, Member):
            obj = self.eval(node.object)

            if (
                isinstance(obj, dict)
                and node.name in obj
            ):
                return obj[node.name]

            try:
                return getattr(obj, node.name)
            except AttributeError as error:
                raise LTH03RuntimeError(
                    f"unknown member '{node.name}'"
                ) from error

        if isinstance(node, Index):
            obj = self.eval(node.object)
            index = self.eval(node.index)

            try:
                return obj[index]
            except (
                KeyError,
                IndexError,
                TypeError,
            ) as error:
                raise LTH03RuntimeError(
                    "invalid index"
                ) from error

        if isinstance(node, Unary):
            value = self.eval(node.operand)

            if node.op == "not":
                return not bool(value)

            if node.op == "-":
                return -value

        if isinstance(node, Binary):
            if node.op == "and":
                left = bool(self.eval(node.left))

                if not left:
                    return False

                return bool(
                    self.eval(node.right)
                )

            if node.op == "or":
                left = bool(self.eval(node.left))

                if left:
                    return True

                return bool(
                    self.eval(node.right)
                )

            left = self.eval(node.left)
            right = self.eval(node.right)

            operations = {
                "+": lambda: left + right,
                "-": lambda: left - right,
                "*": lambda: left * right,
                "/": lambda: left / right,
                "%": lambda: left % right,
                "==": lambda: left == right,
                "!=": lambda: left != right,
                "<": lambda: left < right,
                "<=": lambda: left <= right,
                ">": lambda: left > right,
                ">=": lambda: left >= right,
            }

            try:
                return operations[node.op]()
            except ZeroDivisionError as error:
                raise LTH03RuntimeError(
                    "division by zero"
                ) from error
            except KeyError as error:
                raise LTH03RuntimeError(
                    f"unsupported operator '{node.op}'"
                ) from error

        if isinstance(node, Call):
            args = [
                self.eval(arg)
                for arg in node.args
            ]

            if node.name == "len" and len(args) == 1:
                return len(args[0])

            if node.name == "bool" and len(args) == 1:
                return bool(args[0])

            raise LTH03RuntimeError(
                f"unknown function '{node.name}'"
            )

        raise LTH03RuntimeError(
            f"unsupported expression {node!r}"
        )

    def assign(self, name, operator, expression):
        value = self.eval(expression)

        if operator == "=":
            result = value

        else:
            if name not in self.state.values:
                raise LTH03RuntimeError(
                    f"unknown value '{name}'"
                )

            old = self.state.values[name]

            operations = {
                "+=": lambda: old + value,
                "-=": lambda: old - value,
                "*=": lambda: old * value,
                "/=": lambda: old / value,
            }

            try:
                result = operations[operator]()
            except ZeroDivisionError as error:
                raise LTH03RuntimeError(
                    "division by zero"
                ) from error
            except KeyError as error:
                raise LTH03RuntimeError(
                    f"unsupported assignment operator "
                    f"'{operator}'"
                ) from error

        self.state.values[name] = result

    def run(self, program):
        from .ast import Assignment, Rule

        for statement in program.statements:
            if isinstance(statement, Assignment):
                self.assign(
                    statement.name,
                    statement.op,
                    statement.expr,
                )

        for statement in program.statements:
            if isinstance(statement, Rule):
                if bool(self.eval(statement.condition)):
                    for action in statement.actions:
                        self.assign(
                            action.name,
                            action.op,
                            action.expr,
                        )

        return self.state
