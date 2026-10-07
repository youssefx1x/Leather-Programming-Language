from dataclasses import dataclass, field


@dataclass
class BaseRuntimeState:
    bases: dict = field(default_factory=dict)
    flows: dict = field(default_factory=dict)


class BaseFlowRuntime:
    def __init__(self):
        self.state = BaseRuntimeState()

    def execute(self, ir):
        self.state = BaseRuntimeState()

        active_base = None
        active_flow = None

        for instruction in ir.instructions:
            opcode = instruction.opcode
            operands = instruction.operands

            if opcode == "BASE_BEGIN":
                name, service = operands

                active_base = name

                self.state.bases[name] = {
                    "service": service,
                    "options": {},
                }

            elif opcode == "BASE_OPTION":
                base_name, key, value = operands

                if base_name not in self.state.bases:
                    raise RuntimeError(
                        f"unknown base '{base_name}'"
                    )

                self.state.bases[
                    base_name
                ]["options"][key] = value

            elif opcode == "BASE_END":
                active_base = None

            elif opcode == "EXTEND_BASE":
                name, base_name = operands

                if base_name not in self.state.bases:
                    raise RuntimeError(
                        f"unknown base '{base_name}'"
                    )

                parent = self.state.bases[base_name]

                self.state.bases[name] = {
                    "service": parent["service"],
                    "options": dict(
                        parent["options"]
                    ),
                    "extends": base_name,
                }

            elif opcode == "EXTENSION_OPTION":
                name, key, value = operands

                if name not in self.state.bases:
                    raise RuntimeError(
                        f"unknown extension '{name}'"
                    )

                self.state.bases[
                    name
                ]["options"][key] = value

            elif opcode == "FLOW_BEGIN":
                name = operands[0]

                active_flow = name

                self.state.flows[name] = []

            elif opcode == "FLOW_STEP":
                flow_name, step = operands

                if flow_name not in self.state.flows:
                    raise RuntimeError(
                        f"unknown flow '{flow_name}'"
                    )

                self.state.flows[
                    flow_name
                ].append(step)

            elif opcode == "FLOW_END":
                active_flow = None

            else:
                raise RuntimeError(
                    f"unsupported base/flow opcode "
                    f"'{opcode}'"
                )

        return self.state
