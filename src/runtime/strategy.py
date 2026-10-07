from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimeStrategy:
    name: str
    target_kind: str
    target_name: str
    reason: str


class RuntimeStrategyResolver:
    """
    Convert OPTIMIZATION_HINT instructions into
    explicit runtime strategies.
    """

    def resolve(self, ir):
        strategies = []

        for instruction in ir.instructions:
            if instruction.opcode != "OPTIMIZATION_HINT":
                continue

            kind, name, strategy = instruction.operands

            strategies.append(
                RuntimeStrategy(
                    name=strategy,
                    target_kind=kind,
                    target_name=name,
                    reason=(
                        "selected by adaptive optimizer"
                    ),
                )
            )

        return strategies
