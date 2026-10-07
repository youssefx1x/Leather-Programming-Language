from dataclasses import dataclass


@dataclass(frozen=True)
class EvidenceEvent:
    kind: str
    message: str
    data: dict


class ExecutionEvidence:
    def __init__(self, trace):
        self.trace = trace

    def events(self):
        return [
            EvidenceEvent(
                kind=event.kind,
                message=event.message,
                data=event.data,
            )
            for event in self.trace.events
        ]

    def find(self, kind=None):
        if kind is None:
            return self.events()

        return [
            event
            for event in self.events()
            if event.kind == kind
        ]

    def why_rule_activated(self, rule_name):
        for event in self.trace.events:
            if (
                event.kind == "ACTIVATE"
                and rule_name in event.message
            ):
                return event.message

        return None

    def changes(self, target=None):
        results = self.find("CHANGE")

        if target is None:
            return results

        return [
            event
            for event in results
            if event.message.startswith(target + ":")
        ]

    def describe(self):
        lines = ["EXECUTION EVIDENCE"]

        for event in self.trace.events:
            lines.append(
                f"  {event.kind}: {event.message}"
            )

        return "\n".join(lines)
