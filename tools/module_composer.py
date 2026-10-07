from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer
from src.semantic.builder import SemanticBuilder


class ModuleCompositionError(Exception):
    pass


class ModuleComposer:
    def compose(self, modules):
        statements = []

        for module in modules:
            try:
                tokens = Lexer(
                    module.source
                ).tokenize()

                program = Parser(
                    tokens
                ).parse()

            except Exception as error:
                raise ModuleCompositionError(
                    f"failed to parse module "
                    f"'{module.path}': {error}"
                ) from error

            statements.extend(
                program.statements
            )

        class ComposedProgram:
            pass

        result = ComposedProgram()
        result.statements = statements

        return result

    def analyze(self, program):
        analyzer = SemanticAnalyzer()
        errors = analyzer.analyze(program)

        if errors:
            messages = "\n".join(
                error.message
                for error in errors
            )

            raise ModuleCompositionError(
                messages
            )

        return SemanticBuilder().build(
            program
        )
