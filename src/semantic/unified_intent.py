from dataclasses import dataclass, field


@dataclass
class UnifiedIntentContext:
    slots: dict = field(default_factory=dict)
    decisions: dict = field(default_factory=dict)

    def set_slot(self, name, value):
        self.slots[name] = value

    def set_decision(self, name, value, reason=None):
        self.decisions[name] = {
            "value": value,
            "reason": reason,
        }

    def get_slot(self, name, default=None):
        return self.slots.get(name, default)

    def get_decision(self, name, default=None):
        return self.decisions.get(name, default)

    def describe(self):
        lines = ["UNIFIED INTENT"]

        if self.slots:
            lines.append("  SLOTS")
            for name, value in self.slots.items():
                lines.append(
                    f"    {name} = {value}"
                )

        if self.decisions:
            lines.append("  DECISIONS")
            for name, decision in self.decisions.items():
                lines.append(
                    f"    {name} = {decision['value']}"
                )

                if decision["reason"]:
                    lines.append(
                        f"      reason = {decision['reason']}"
                    )

        return "\n".join(lines)
