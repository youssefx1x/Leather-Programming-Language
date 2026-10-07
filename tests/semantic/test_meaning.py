from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer
from src.semantic.meaning import MeaningGraph


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

graph = MeaningGraph()

for statement in program.statements:
    if statement.__class__.__name__ == "Assignment":
        graph.add_definition(
            statement.name,
            statement.value,
        )

    elif statement.__class__.__name__ == "Rule":
        graph.add_rule(statement)

print("MEANING GRAPH:")
print(graph.describe())
