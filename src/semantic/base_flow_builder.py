from src.parser.base_flow import (
    Base,
    BaseExtension,
    Flow,
)

from src.semantic.base_flow_model import (
    SemanticBaseFlowProgram,
    SemanticBase,
    SemanticBaseExtension,
    SemanticFlow,
    SemanticOption,
)


class BaseFlowBuilder:
    def build(self, program):
        result = SemanticBaseFlowProgram()

        for statement in program.statements:

            if isinstance(statement, Base):
                result.bases.append(
                    SemanticBase(
                        name=statement.name,
                        service=statement.service,
                        options=tuple(
                            SemanticOption(
                                name=name,
                                value=self._value(value),
                            )
                            for name, value in statement.options
                        ),
                    )
                )

            elif isinstance(statement, BaseExtension):
                result.extensions.append(
                    SemanticBaseExtension(
                        name=statement.name,
                        base_name=statement.base_name,
                        options=tuple(
                            SemanticOption(
                                name=name,
                                value=self._value(value),
                            )
                            for name, value in statement.options
                        ),
                    )
                )

            elif isinstance(statement, Flow):
                result.flows.append(
                    SemanticFlow(
                        name=statement.name,
                        steps=tuple(statement.steps),
                    )
                )

        return result

    def _value(self, value):
        if hasattr(value, "value"):
            raw = value.value

            if str(raw).lower() == "true":
                return True

            if str(raw).lower() == "false":
                return False

            try:
                return int(raw)
            except ValueError:
                pass

            try:
                return float(raw)
            except ValueError:
                pass

            return raw

        return value
