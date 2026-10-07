from dataclasses import dataclass


@dataclass(frozen=True)
class IRValidationError:
    index: int
    message: str


class IRValidator:
    def validate(self, ir):
        errors = []
        inside_rule = False
        saw_condition = False
        saw_effect = False

        for index, instruction in enumerate(ir.instructions):
            opcode = instruction.opcode

            if opcode == "RULE_BEGIN":
                if inside_rule:
                    errors.append(
                        IRValidationError(
                            index,
                            "nested RULE_BEGIN is not allowed",
                        )
                    )

                inside_rule = True
                saw_condition = False
                saw_effect = False

            elif opcode == "CHECK_MEMBER":
                if not inside_rule:
                    errors.append(
                        IRValidationError(
                            index,
                            "CHECK_MEMBER must be inside a rule",
                        )
                    )
                else:
                    saw_condition = True

            elif opcode == "IF_TRUE":
                if not inside_rule:
                    errors.append(
                        IRValidationError(
                            index,
                            "IF_TRUE must be inside a rule",
                        )
                    )

                if not saw_condition:
                    errors.append(
                        IRValidationError(
                            index,
                            "IF_TRUE requires a condition",
                        )
                    )

            elif opcode == "EFFECT":
                if not inside_rule:
                    errors.append(
                        IRValidationError(
                            index,
                            "EFFECT must be inside a rule",
                        )
                    )
                else:
                    saw_effect = True

            elif opcode == "RULE_END":
                if not inside_rule:
                    errors.append(
                        IRValidationError(
                            index,
                            "RULE_END without RULE_BEGIN",
                        )
                    )
                else:
                    if not saw_condition:
                        errors.append(
                            IRValidationError(
                                index,
                                "rule has no condition",
                            )
                        )

                    if not saw_effect:
                        errors.append(
                            IRValidationError(
                                index,
                                "rule has no effect",
                            )
                        )

                    inside_rule = False

            elif opcode == "DEFINE":
                if inside_rule:
                    errors.append(
                        IRValidationError(
                            index,
                            "DEFINE cannot appear inside a rule",
                        )
                    )

            else:
                errors.append(
                    IRValidationError(
                        index,
                        f"unknown opcode '{opcode}'",
                    )
                )

        if inside_rule:
            errors.append(
                IRValidationError(
                    len(ir.instructions),
                    "rule was not closed with RULE_END",
                )
            )

        return errors
