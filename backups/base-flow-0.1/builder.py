from src.parser.parser import (
    Assignment,
    NumberValue,
    StringValue,
    Rule,
)

from src.semantic.model import (
    SemanticProgram,
    SemanticDefinition,
    SemanticValue,
    SemanticCondition,
    SemanticEffect,
    SemanticRule,
)


class SemanticBuilder:
    def build(self, program):
        result = SemanticProgram()

        for statement in program.statements:
            if isinstance(statement, Assignment):
                result.definitions.append(
                    SemanticDefinition(
                        name=statement.name,
                        value=self._value(statement.value),
                    )
                )

            elif isinstance(statement, Rule):
                result.rules.append(
                    SemanticRule(
                        name=statement.name,
                        condition=SemanticCondition(
                            object_name=statement.condition.object_name,
                            member_name=statement.condition.member_name,
                        ),
                        effect=SemanticEffect(
                            target=statement.action_target,
                            operator=statement.action_operator,
                            value=self._value(statement.action_value),
                        ),
                    )
                )

        return result

    def _value(self, value):
        if isinstance(value, NumberValue):
            return SemanticValue(
                kind="number",
                value=value.value,
            )

        if isinstance(value, StringValue):
            return SemanticValue(
                kind="string",
                value=value.value,
            )

        raise TypeError(
            f"unsupported AST value: {type(value).__name__}"
        )
