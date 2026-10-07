from src.runtime.runtime import LTHRuntime
from src.runtime.trace import ExecutionTrace


class ExplainableRuntime(LTHRuntime):
    def __init__(self):
        super().__init__()
        self.trace = ExecutionTrace()

    def execute(self, ir, context=None):
        self.trace = ExecutionTrace()

        self.state = type(self.state)(
            values={},
            context=context or {},
        )

        inside_rule = False
        rule_active = False
        current_rule = None

        for instruction in ir.instructions:
            opcode = instruction.opcode
            operands = instruction.operands

            if opcode == "DEFINE":
                name, kind, value = operands

                converted = self._convert_value(
                    kind,
                    value,
                )

                self.state.values[name] = converted

                self.trace.record(
                    "DEFINE",
                    f"{name} = {converted}",
                )

            elif opcode == "RULE_BEGIN":
                inside_rule = True
                rule_active = False
                current_rule = operands[0]

                self.trace.record(
                    "RULE",
                    f"{current_rule} started",
                )

            elif opcode == "CHECK_MEMBER":
                if not inside_rule:
                    raise RuntimeError(
                        "CHECK_MEMBER outside rule"
                    )

                object_name, member_name = operands

                object_value = self.state.context.get(
                    object_name,
                    {},
                )

                result = bool(
                    isinstance(object_value, dict)
                    and object_value.get(member_name)
                )

                rule_active = result

                self.trace.record(
                    "CHECK",
                    f"{object_name}.{member_name} = {str(result).lower()}",
                )

            elif opcode == "IF_TRUE":
                if not inside_rule:
                    raise RuntimeError(
                        "IF_TRUE outside rule"
                    )

                if rule_active:
                    self.trace.record(
                        "ACTIVATE",
                        f"rule {current_rule} activated",
                    )
                else:
                    self.trace.record(
                        "SKIP",
                        f"rule {current_rule} skipped",
                    )

            elif opcode == "EFFECT":
                if not inside_rule:
                    raise RuntimeError(
                        "EFFECT outside rule"
                    )

                if rule_active:
                    target, operator, value = operands

                    if target not in self.state.values:
                        raise RuntimeError(
                            f"unknown runtime value '{target}'"
                        )

                    before = self.state.values[target]

                    self._apply_effect(
                        target,
                        operator,
                        value,
                    )

                    after = self.state.values[target]

                    self.trace.record(
                        "EFFECT",
                        f"{target} {operator} {value}",
                    )

                    self.trace.record(
                        "CHANGE",
                        f"{target}: {before} -> {after}",
                    )

            elif opcode == "RULE_END":
                inside_rule = False
                rule_active = False

                self.trace.record(
                    "RULE",
                    f"{current_rule} ended",
                )

                current_rule = None

            else:
                raise RuntimeError(
                    f"unknown opcode '{opcode}'"
                )

        return self.state
