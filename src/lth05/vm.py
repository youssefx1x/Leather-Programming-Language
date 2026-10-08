from __future__ import annotations

from dataclasses import dataclass, field
from copy import deepcopy
from collections.abc import Mapping

from .model import ProgramCode
from .profiler import ExecutionProfile
from .specialized import SpecializationCache, generic_binary


class VMError(Exception):
    pass


@dataclass
class VMResult:
    values: dict
    profile: ExecutionProfile
    trace: list[str] = field(default_factory=list)


class VirtualMachine:
    def __init__(self, step_limit=1_000_000):
        self.step_limit = step_limit
        self.specialized = SpecializationCache()

    def run(self, code: ProgramCode, context=None, trace=False):
        context = dict(context or {})
        values = {}
        stack = []
        profile = ExecutionProfile()
        instructions = code.instructions
        constants = code.constants
        names = code.names

        builtins = {
            "len": len,
            "bool": bool,
        }

        ip = 0
        steps = 0

        while ip < len(instructions):
            if steps >= self.step_limit:
                raise VMError(
                    f"step limit exceeded: {self.step_limit}"
                )

            ins = instructions[ip]
            steps += 1
            profile.record_opcode(ins.op)

            if trace:
                profile.add_trace(
                    f"{ip:04d} {ins.op} {ins.arg!r} stack={len(stack)}"
                )

            op = ins.op

            if op == "NOP":
                ip += 1
                continue

            if op == "CONST":
                stack.append(deepcopy(constants[ins.arg]))
                ip += 1
                profile.record_stack(len(stack))
                continue

            if op == "LOAD":
                name = names[ins.arg]

                if name in values:
                    stack.append(values[name])
                elif name in context:
                    stack.append(context[name])
                elif name in builtins:
                    stack.append(builtins[name])
                else:
                    raise VMError(f"unknown variable: {name}")

                ip += 1
                profile.record_stack(len(stack))
                continue

            if op == "STORE":
                name = names[ins.arg]

                if not stack:
                    raise VMError(
                        f"empty stack on STORE {name}"
                    )

                values[name] = stack.pop()
                ip += 1
                continue

            if op == "LOAD_MEMBER":
                if not stack:
                    raise VMError("empty stack on LOAD_MEMBER")

                obj = stack.pop()
                name = ins.arg

                try:
                    if isinstance(obj, Mapping):
                        value = obj[name]
                    else:
                        value = getattr(obj, name)
                except (KeyError, AttributeError) as error:
                    raise VMError(
                        f"member '{name}' not found"
                    ) from error

                stack.append(value)
                ip += 1
                profile.record_stack(len(stack))
                continue

            if op == "LOAD_INDEX":
                if len(stack) < 2:
                    raise VMError("stack underflow on LOAD_INDEX")

                index = stack.pop()
                obj = stack.pop()
                stack.append(obj[index])

                ip += 1
                profile.record_stack(len(stack))
                continue

            if op == "BUILD_LIST":
                count = ins.arg

                if len(stack) < count:
                    raise VMError("stack underflow on BUILD_LIST")

                values_list = stack[-count:] if count else []
                if count:
                    del stack[-count:]

                stack.append(list(values_list))
                ip += 1
                profile.record_stack(len(stack))
                continue

            if op == "BUILD_MAP":
                count = ins.arg

                if len(stack) < count * 2:
                    raise VMError("stack underflow on BUILD_MAP")

                result = {}

                for _ in range(count):
                    value = stack.pop()
                    key = stack.pop()
                    result[key] = value

                stack.append(result)
                ip += 1
                profile.record_stack(len(stack))
                continue

            if op == "UNARY":
                if not stack:
                    raise VMError("stack underflow on UNARY")

                value = stack.pop()
                operator = ins.arg

                if operator in {"not", "!"}:
                    result = not value
                elif operator == "+":
                    result = +value
                elif operator == "-":
                    result = -value
                else:
                    raise VMError(
                        f"unsupported unary operator: {operator}"
                    )

                stack.append(result)
                ip += 1
                profile.record_stack(len(stack))
                continue

            if op == "BINARY":
                if len(stack) < 2:
                    raise VMError("stack underflow on BINARY")

                right = stack.pop()
                left = stack.pop()

                result = self.specialized.execute(
                    ins.arg,
                    left,
                    right,
                    profile=profile,
                )

                stack.append(result)
                ip += 1
                profile.record_stack(len(stack))
                continue

            if op == "CALL":
                count = ins.arg

                if len(stack) < count + 1:
                    raise VMError("stack underflow on CALL")

                args = stack[-count:] if count else []
                if count:
                    del stack[-count:]

                function = stack.pop()

                try:
                    result = function(*args)
                except Exception as error:
                    raise VMError(
                        f"call failed: {error}"
                    ) from error

                stack.append(result)
                ip += 1
                profile.record_stack(len(stack))
                continue

            if op == "JUMP_IF_FALSE":
                if not stack:
                    raise VMError(
                        "stack underflow on JUMP_IF_FALSE"
                    )

                condition = stack.pop()

                if not condition:
                    ip = ins.arg
                else:
                    ip += 1

                continue

            if op == "JUMP":
                ip = ins.arg
                continue

            if op == "POP":
                if not stack:
                    raise VMError("stack underflow on POP")
                stack.pop()
                ip += 1
                continue

            if op == "HALT":
                break

            raise VMError(f"unknown opcode: {op}")

        return VMResult(
            values=values,
            profile=profile,
            trace=list(profile.trace),
        )
