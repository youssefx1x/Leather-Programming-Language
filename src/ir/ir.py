from dataclasses import dataclass, field


@dataclass(frozen=True)
class IRInstruction:
    opcode: str
    operands: tuple = ()


@dataclass
class LTHIR:
    instructions: list[IRInstruction] = field(default_factory=list)

    def emit(self, opcode, *operands):
        instruction = IRInstruction(
            opcode=opcode,
            operands=tuple(operands),
        )

        self.instructions.append(instruction)
        return instruction

    def describe(self):
        lines = ["LTH IR"]

        for index, instruction in enumerate(self.instructions):
            if instruction.operands:
                operands = " ".join(
                    str(value)
                    for value in instruction.operands
                )

                lines.append(
                    f"  {index:04d} "
                    f"{instruction.opcode} "
                    f"{operands}"
                )
            else:
                lines.append(
                    f"  {index:04d} "
                    f"{instruction.opcode}"
                )

        return "\n".join(lines)
