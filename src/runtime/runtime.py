from dataclasses import dataclass, field


@dataclass
class RuntimeState:
    values: dict = field(default_factory=dict)
    context: dict = field(default_factory=dict)


class RuntimeErrorLTH(Exception):
    pass


class LTHRuntime:
    def __init__(self):
        self.state = RuntimeState()

    def execute(self, ir, context=None):
        self.state = RuntimeState(
            values={},
            context=context or {},
        )

        inside_rule = False
        rule_active = False

        for instruction in ir.instructions:
            opcode = instruction.opcode
            operands = instruction.operands

            if opcode == "DEFINE":
                name, kind, value = operands

                self.state.values[name] = self._convert_value(
                    kind,
                    value,
                )

            elif opcode == "RULE_BEGIN":
                inside_rule = True
                rule_active = False

            elif opcode == "CHECK_MEMBER":
                if not inside_rule:
                    raise RuntimeErrorLTH(
                        "CHECK_MEMBER outside rule"
                    )

                object_name, member_name = operands

                object_value = self.state.context.get(
                    object_name,
                    {},
                )

                rule_active = bool(
                    isinstance(object_value, dict)
                    and object_value.get(member_name)
                )

            elif opcode == "IF_TRUE":
                if not inside_rule:
                    raise RuntimeErrorLTH(
                        "IF_TRUE outside rule"
                    )

            elif opcode == "EFFECT":
                if not inside_rule:
                    raise RuntimeErrorLTH(
                        "EFFECT outside rule"
                    )

                if rule_active:
                    target, operator, value = operands

                    self._apply_effect(
                        target,
                        operator,
                        value,
                    )

            elif opcode == "RULE_END":
                inside_rule = False
                rule_active = False

            else:
                raise RuntimeErrorLTH(
                    f"unknown opcode '{opcode}'"
                )

        return self.state

    def _convert_value(self, kind, value):
        if kind == "number":
            return float(value)

        if kind == "string":
            return value

        raise RuntimeErrorLTH(
            f"unsupported value kind '{kind}'"
        )

    def _apply_effect(self, target, operator, value):
        if target not in self.state.values:
            raise RuntimeErrorLTH(
                f"unknown runtime value '{target}'"
            )

        current = self.state.values[target]

        if operator == "*=":
            self.state.values[target] = (
                current * float(value)
            )
            return

        raise RuntimeErrorLTH(
            f"unsupported effect operator '{operator}'"
        )
