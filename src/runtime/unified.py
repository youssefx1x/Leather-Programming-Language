from src.ir.ir import LTHIR
from src.runtime.runtime import LTHRuntime


class UnifiedRuntime(LTHRuntime):
    """
    Runtime adapter for Unified LTH IR.

    Unified semantic declarations such as BASE, FLOW and SYSTEM
    are understood here, while core executable instructions are
    delegated to the original LTHRuntime.
    """

    UNIFIED_METADATA_OPCODES = {
        "BASE_BEGIN",
        "BASE_OPTION",
        "BASE_END",
        "EXTEND_BASE",
        "EXTENSION_OPTION",
        "FLOW_BEGIN",
        "FLOW_STEP",
        "FLOW_END",
        "SYSTEM_BEGIN",
        "SYSTEM_COMPONENT",
        "SYSTEM_END",
        "OPTIMIZATION_HINT",
    }

    def __init__(self):
        super().__init__()

        self.base_metadata = []
        self.flow_metadata = []
        self.system_metadata = []
        self.optimization_hints = []

    def execute(self, ir, context=None):
        executable = LTHIR()

        self.base_metadata = []
        self.flow_metadata = []
        self.system_metadata = []
        self.optimization_hints = []

        for instruction in ir.instructions:
            opcode = instruction.opcode

            if opcode in self.UNIFIED_METADATA_OPCODES:
                self._capture_metadata(instruction)
                continue

            executable.instructions.append(instruction)

        return super().execute(
            executable,
            context=context,
        )

    def _capture_metadata(self, instruction):
        opcode = instruction.opcode
        operands = instruction.operands

        if opcode.startswith("BASE") or opcode.startswith("EXTEND") or opcode.startswith("EXTENSION"):
            self.base_metadata.append(
                (opcode, operands)
            )
            return

        if opcode.startswith("FLOW"):
            self.flow_metadata.append(
                (opcode, operands)
            )
            return

        if opcode.startswith("SYSTEM"):
            self.system_metadata.append(
                (opcode, operands)
            )
            return

        if opcode == "OPTIMIZATION_HINT":
            self.optimization_hints.append(
                operands
            )
