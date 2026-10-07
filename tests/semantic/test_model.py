from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer
from src.semantic.builder import SemanticBuilder


source = '''price = 150.5
rule discount when customer.vip -> price *= 0.9
'''

tokens = Lexer(source).tokenize()
program = Parser(tokens).parse()

analyzer = SemanticAnalyzer()
errors = analyzer.analyze(program)

if errors:
    for error in errors:
        print(error.message)
    raise SystemExit(1)

semantic = SemanticBuilder().build(program)

print("DEFINITIONS:")

for definition in semantic.definitions:
    print(
        f"{definition.name} = "
        f"{definition.value.value}"
    )

print("RULES:")

for rule in semantic.rules:
    print(
        f"{rule.name}: "
        f"when {rule.condition.object_name}."
        f"{rule.condition.member_name} "
        f"-> "
        f"{rule.effect.target} "
        f"{rule.effect.operator} "
        f"{rule.effect.value.value}"
    )
