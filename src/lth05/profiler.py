from dataclasses import dataclass, field


@dataclass
class ExecutionProfile:
    instruction_count: int = 0
    max_stack: int = 0
    opcode_counts: dict[str, int] = field(default_factory=dict)
    specialization_hits: int = 0
    specialization_misses: int = 0
    trace: list[str] = field(default_factory=list)

    def record_opcode(self, opcode):
        self.instruction_count += 1
        self.opcode_counts[opcode] = self.opcode_counts.get(opcode, 0) + 1

    def record_stack(self, size):
        if size > self.max_stack:
            self.max_stack = size

    def add_trace(self, message):
        self.trace.append(message)

    def summary(self):
        return {
            "instructions": self.instruction_count,
            "max_stack": self.max_stack,
            "opcodes": dict(self.opcode_counts),
            "specialization_hits": self.specialization_hits,
            "specialization_misses": self.specialization_misses,
        }
