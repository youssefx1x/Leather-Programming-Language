from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer


source = '''price = 150.5
rule discount when customer.vip -> price *= 0.9
'''

tokens = Lexer(source).tokenize()
program = Parser(tokens).parse()

analyzer = SemanticAnalyzer()
errors = analyzer.analyze(program)

print("SYMBOLS:")
print(analyzer.symbols)

print("ERRORS:")
for error in errors:
    print(error.message)
