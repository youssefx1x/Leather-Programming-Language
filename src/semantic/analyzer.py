from dataclasses import dataclass


@dataclass
class SemanticError:
    message: str


class SemanticAnalyzer:
    def __init__(self):
        self.symbols = {}
        self.errors = []

    def analyze(self, program):
        self.symbols = {}
        self.errors = []

        for statement in program.statements:
            if statement.__class__.__name__ == "Assignment":
                self._analyze_assignment(statement)

            elif statement.__class__.__name__ == "Rule":
                self._analyze_rule(statement)

        return self.errors

    def _analyze_assignment(self, statement):
        self.symbols[statement.name] = statement.value

    def _analyze_rule(self, statement):
        target = statement.action_target

        if target not in self.symbols:
            self.errors.append(
                SemanticError(
                    f"unknown value '{target}' in rule "
                    f"'{statement.name}'"
                )
            )
