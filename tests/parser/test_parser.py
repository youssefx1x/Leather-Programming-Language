from src.lexer.lexer import Lexer
from src.parser.parser import Parser


source = '''name = "Leather"
age = 20
price = 150.5
'''

tokens = Lexer(source).tokenize()
program = Parser(tokens).parse()

print(program)
