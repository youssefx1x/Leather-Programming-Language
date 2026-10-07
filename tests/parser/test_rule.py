from src.lexer.lexer import Lexer
from src.parser.parser import Parser


source = '''rule discount when customer.vip -> price *= 0.9
'''

tokens = Lexer(source).tokenize()

try:
    program = Parser(tokens).parse()
    print(program)
except Exception as error:
    print(type(error).__name__)
    print(error)
