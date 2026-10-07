from dataclasses import dataclass


@dataclass(frozen=True)
class SystemValidationError:
    index: int
    message: str


class SystemValidator:
    def validate(self, ir):
        errors = []

        active_system = None
        known_systems = set()

        for index, instruction in enumerate(ir.instructions):
            opcode = instruction.opcode
            operands = instruction.operands

            if opcode == "SYSTEM_BEGIN":
                name = operands[0]

                if active_system is not None:
                    errors.append(
                        SystemValidationError(
                            index,
                            "nested SYSTEM_BEGIN",
                        )
                    )

                if name in known_systems:
                    errors.append(
                        SystemValidationError(
                            index,
                            f"duplicate system '{name}'",
                        )
                    )

                active_system = name

            elif opcode == "SYSTEM_COMPONENT":
                if active_system is None:
                    errors.append(
                        SystemValidationError(
                            index,
                            "SYSTEM_COMPONENT outside system",
                        )
                    )
                elif operands[0] != active_system:
                    errors.append(
                        SystemValidationError(
                            index,
                            "component belongs to another system",
                        )
                    )

            elif opcode == "SYSTEM_END":
                if active_system is None:
                    errors.append(
                        SystemValidationError(
                            index,
                            "SYSTEM_END without SYSTEM_BEGIN",
                        )
                    )
                else:
                    known_systems.add(active_system)
                    active_system = None

            else:
                errors.append(
                    SystemValidationError(
                        index,
                        f"unknown system opcode '{opcode}'",
                    )
                )

        if active_system is not None:
            errors.append(
                SystemValidationError(
                    len(ir.instructions),
                    "system was not closed",
                )
            )

        return errors
