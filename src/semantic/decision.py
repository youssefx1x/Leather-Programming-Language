from dataclasses import dataclass


@dataclass(frozen=True)
class Decision:
    slot: str
    value: object
    reason: str


class DecisionEngine:
    def decide(self, slot, context=None):
        context = context or {}

        if slot.state.value == "fixed":
            return Decision(
                slot=slot.name,
                value=slot.value,
                reason="value was explicitly fixed by the user",
            )

        if slot.state.value == "open":
            return Decision(
                slot=slot.name,
                value=None,
                reason="decision remains open for a later planning stage",
            )

        return self._auto_decide(slot, context)

    def _auto_decide(self, slot, context):
        if slot.name == "execution.mode":
            memory_mb = context.get("memory_mb")

            if memory_mb is not None and memory_mb < 1024:
                return Decision(
                    slot=slot.name,
                    value="streaming",
                    reason=(
                        "available memory is below 1024 MB, "
                        "so streaming reduces memory pressure"
                    ),
                )

            return Decision(
                slot=slot.name,
                value="adaptive",
                reason=(
                    "no restrictive memory condition was detected, "
                    "so execution can remain adaptive"
                ),
            )

        return Decision(
            slot=slot.name,
            value="deferred",
            reason=(
                "no decision rule is defined yet for this intent slot"
            ),
        )
