from dataclasses import dataclass
from typing import Callable

from src.sea import SEAClass, SEAValue


@dataclass(frozen=True)
class SEARule:
    operation: str
    name: str
    matcher: Callable
    resolver: Callable

    def matches(self, left, right):
        return self.matcher(left, right)

    def apply(self, left, right):
        return self.resolver(left, right)


class SEARuleRegistry:
    def __init__(self):
        self._rules = {}

    def register(self, rule):
        self._rules.setdefault(
            rule.operation,
            [],
        ).append(rule)

    def resolve(self, operation, left, right):
        rules = self._rules.get(operation, [])

        for rule in rules:
            if rule.matches(left, right):
                return rule.apply(left, right)

        return None

    def rules_for(self, operation):
        return tuple(
            self._rules.get(operation, ())
        )


def exceptional_operand_match(left, right):
    return (
        left.is_exceptional
        or right.is_exceptional
    )


def exceptional_operand_resolve(left, right, operation):
    return SEAValue.exceptional(
        operation,
        (left, right),
        "exceptional_operand",
    )


def register_default_rules(registry):
    operations = (
        "add",
        "subtract",
        "multiply",
        "divide",
    )

    for operation in operations:
        registry.register(
            SEARule(
                operation=operation,
                name=f"{operation}_exceptional_propagation",
                matcher=exceptional_operand_match,
                resolver=lambda left, right, op=operation:
                    exceptional_operand_resolve(
                        left,
                        right,
                        op,
                    ),
            )
        )

    return registry
