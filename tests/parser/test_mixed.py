from src.lexer.lexer import Lexer
from src.parser.parser import Parser


source = '''price = 150.5
rule discount when customer.vip -> price *= 0.9
'''

tokens = Lexer(source).tokenize()
program = Parser(tokens).parse()

print(program)
