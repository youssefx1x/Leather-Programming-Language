from .model import BytecodeProgram, Instruction


class BytecodeOptimizer:
    def optimize(self, program):
        instructions = []
        seen_halt = False

        for instruction in program.instructions:
            if instruction.op == "NOP":
                continue

            if seen_halt:
                continue

            instructions.append(instruction)

            if instruction.op == "HALT":
                seen_halt = True

        if not instructions:
            instructions.append(
                Instruction("HALT")
            )

        if instructions[-1].op != "HALT":
            instructions.append(
                Instruction("HALT")
            )

        return BytecodeProgram(
            instructions=tuple(instructions),
            source_hash=program.source_hash,
            prepared_source=program.prepared_source,
            statement_count=program.statement_count,
            flow_names=program.flow_names,
            system_names=program.system_names,
            base_names=program.base_names,
            optimized=True,
        )

    def validate(self, program):
        if not program.instructions:
            raise ValueError(
                "bytecode program is empty"
            )

        halt_positions = [
            index
            for index, instruction
            in enumerate(program.instructions)
            if instruction.op == "HALT"
        ]

        if len(halt_positions) != 1:
            raise ValueError(
                "bytecode must contain exactly one HALT"
            )

        if halt_positions[0] != (
            len(program.instructions) - 1
        ):
            raise ValueError(
                "HALT must be the final instruction"
            )

        allowed = {
            "EXECUTE",
            "HALT",
            "NOP",
        }

        for instruction in program.instructions:
            if instruction.op not in allowed:
                raise ValueError(
                    f"unknown bytecode op: "
                    f"{instruction.op}"
                )

        return True
