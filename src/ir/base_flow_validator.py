from dataclasses import dataclass


@dataclass(frozen=True)
class BaseFlowValidationError:
    index: int
    message: str


class BaseFlowValidator:
    def validate(self, ir):
        errors = []

        active_base = None
        active_flow = None
        known_bases = set()

        for index, instruction in enumerate(
            ir.instructions
        ):
            opcode = instruction.opcode
            operands = instruction.operands

            if opcode == "BASE_BEGIN":
                name = operands[0]

                if active_base is not None:
                    errors.append(
                        BaseFlowValidationError(
                            index,
                            "nested BASE_BEGIN",
                        )
                    )

                if name in known_bases:
                    errors.append(
                        BaseFlowValidationError(
                            index,
                            f"duplicate base '{name}'",
                        )
                    )

                active_base = name

            elif opcode == "BASE_OPTION":
                if active_base is None:
                    errors.append(
                        BaseFlowValidationError(
                            index,
                            "BASE_OPTION outside base",
                        )
                    )

            elif opcode == "BASE_END":
                if active_base is None:
                    errors.append(
                        BaseFlowValidationError(
                            index,
                            "BASE_END without BASE_BEGIN",
                        )
                    )
                else:
                    known_bases.add(active_base)
                    active_base = None

            elif opcode == "EXTEND_BASE":
                name, base_name = operands

                if base_name not in known_bases:
                    errors.append(
                        BaseFlowValidationError(
                            index,
                            f"unknown base '{base_name}'",
                        )
                    )

            elif opcode == "EXTENSION_OPTION":
                pass

            elif opcode == "FLOW_BEGIN":
                if active_flow is not None:
                    errors.append(
                        BaseFlowValidationError(
                            index,
                            "nested FLOW_BEGIN",
                        )
                    )

                active_flow = operands[0]

            elif opcode == "FLOW_STEP":
                if active_flow is None:
                    errors.append(
                        BaseFlowValidationError(
                            index,
                            "FLOW_STEP outside flow",
                        )
                    )

            elif opcode == "FLOW_END":
                if active_flow is None:
                    errors.append(
                        BaseFlowValidationError(
                            index,
                            "FLOW_END without FLOW_BEGIN",
                        )
                    )
                else:
                    active_flow = None

        if active_base is not None:
            errors.append(
                BaseFlowValidationError(
                    len(ir.instructions),
                    "base was not closed",
                )
            )

        if active_flow is not None:
            errors.append(
                BaseFlowValidationError(
                    len(ir.instructions),
                    "flow was not closed",
                )
            )

        return errors
