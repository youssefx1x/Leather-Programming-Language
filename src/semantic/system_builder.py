from src.parser.system import System
from src.semantic.system_model import (
    SemanticSystem,
    SemanticSystemProgram,
)


class SystemBuilder:
    def build(self, program):
        result = SemanticSystemProgram()

        for statement in program.statements:
            if isinstance(statement, System):
                result.systems.append(
                    SemanticSystem(
                        name=statement.name,
                        components=tuple(statement.components),
                    )
                )

        return result
