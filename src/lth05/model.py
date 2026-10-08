from dataclasses import dataclass, field
from copy import deepcopy


@dataclass
class Instruction:
    op: str
    arg: object = None
    note: str = ""


@dataclass
class ProgramCode:
    instructions: list[Instruction] = field(default_factory=list)
    constants: list[object] = field(default_factory=list)
    names: list[str] = field(default_factory=list)

    def clone(self):
        return ProgramCode(
            instructions=deepcopy(self.instructions),
            constants=deepcopy(self.constants),
            names=deepcopy(self.names),
        )

    def disassemble(self):
        rows = []
        for index, ins in enumerate(self.instructions):
            arg = ""
            if ins.arg is not None:
                arg = f" {ins.arg!r}"
            suffix = f"  ; {ins.note}" if ins.note else ""
            rows.append(f"{index:04d} {ins.op}{arg}{suffix}")
        return "\n".join(rows)
