class OptimizationIRValidator:
    """
    Validate optimization metadata instructions.
    """

    def validate(self, ir):
        errors = []

        for index, instruction in enumerate(
            ir.instructions
        ):
            if instruction.opcode != "OPTIMIZATION_HINT":
                continue

            operands = instruction.operands

            if len(operands) != 3:
                errors.append(
                    f"{index}: OPTIMIZATION_HINT "
                    "requires kind, name, strategy"
                )
                continue

            kind, name, strategy = operands

            if not kind:
                errors.append(
                    f"{index}: optimization kind is empty"
                )

            if not name:
                errors.append(
                    f"{index}: optimization name is empty"
                )

            if not strategy:
                errors.append(
                    f"{index}: optimization strategy is empty"
                )

        return errors

    def is_valid(self, ir):
        return not self.validate(ir)

    def describe(self, ir):
        errors = self.validate(ir)

        if not errors:
            return "OPTIMIZATION IR VALID"

        lines = ["OPTIMIZATION IR INVALID"]

        for error in errors:
            lines.append(f"  {error}")

        return "\n".join(lines)
