from dataclasses import dataclass
from enum import Enum


class SlotState(Enum):
    FIXED = "fixed"
    OPEN = "open"
    AUTO = "auto"


@dataclass(frozen=True)
class IntentSlot:
    name: str
    state: SlotState
    value: object = None


class Intent:
    def __init__(self):
        self.slots = {}

    def define(self, name, state=SlotState.AUTO, value=None):
        if state == SlotState.FIXED and value is None:
            raise ValueError(
                f"fixed intent slot '{name}' requires a value"
            )

        self.slots[name] = IntentSlot(
            name=name,
            state=state,
            value=value,
        )

    def get(self, name):
        return self.slots[name]

    def describe(self):
        lines = ["INTENT"]

        for slot in self.slots.values():
            if slot.state == SlotState.OPEN:
                lines.append(
                    f"  {slot.name} = OPEN"
                )

            elif slot.state == SlotState.AUTO:
                lines.append(
                    f"  {slot.name} = AUTO"
                )

            else:
                lines.append(
                    f"  {slot.name} = {slot.value}"
                )

        return "\n".join(lines)
