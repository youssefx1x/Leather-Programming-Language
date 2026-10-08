from .model import ProgramCode, Instruction
from .specialized import generic_binary


class OptimizationError(Exception):
    pass


def _constant_fold(code: ProgramCode):
    folded = 0

    for index in range(len(code.instructions) - 2):
        a = code.instructions[index]
        b = code.instructions[index + 1]
        c = code.instructions[index + 2]

        if (
            a.op == "CONST"
            and b.op == "CONST"
            and c.op == "BINARY"
        ):
            left = code.constants[a.arg]
            right = code.constants[b.arg]

            try:
                value = generic_binary(c.arg, left, right)
            except Exception:
                continue

            code.constants.append(value)
            new_index = len(code.constants) - 1

            code.instructions[index] = Instruction(
                "CONST",
                new_index,
                "constant-folded",
            )
            code.instructions[index + 1] = Instruction("NOP")
            code.instructions[index + 2] = Instruction("NOP")
            folded += 1

    return folded


def validate(code: ProgramCode):
    size = len(code.instructions)

    for index, instruction in enumerate(code.instructions):
        if instruction.op in {"JUMP", "JUMP_IF_FALSE"}:
            if not isinstance(instruction.arg, int):
                raise OptimizationError(
                    f"invalid jump target at instruction {index}"
                )

            if instruction.arg < 0 or instruction.arg > size:
                raise OptimizationError(
                    f"jump target {instruction.arg} out of range"
                )

    return True


def optimize(code: ProgramCode):
    optimized = code.clone()

    folded = _constant_fold(optimized)
    validate(optimized)

    return optimized, {
        "constant_folds": folded,
        "instruction_count": len(optimized.instructions),
    }
