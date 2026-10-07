from dataclasses import dataclass, field


@dataclass
class SystemRuntimeState:
    systems: dict = field(default_factory=dict)


class SystemRuntime:
    def __init__(self):
        self.state = SystemRuntimeState()

    def execute(self, ir):
        self.state = SystemRuntimeState()

        active_system = None

        for instruction in ir.instructions:
            opcode = instruction.opcode
            operands = instruction.operands

            if opcode == "SYSTEM_BEGIN":
                name = operands[0]

                active_system = name

                self.state.systems[name] = {
                    "components": [],
                }

            elif opcode == "SYSTEM_COMPONENT":
                system_name, index, component = operands

                if system_name not in self.state.systems:
                    raise RuntimeError(
                        f"unknown system '{system_name}'"
                    )

                self.state.systems[system_name]["components"].append(
                    {
                        "index": index,
                        "name": component,
                    }
                )

            elif opcode == "SYSTEM_END":
                active_system = None

            else:
                raise RuntimeError(
                    f"unsupported system opcode '{opcode}'"
                )

        return self.state
