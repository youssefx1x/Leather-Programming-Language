from src.lexer.lexer import Lexer


source = '''rule discount when customer.vip -> price *= 0.9
'''

tokens = Lexer(source).tokenize()

for token in tokens:
    print(token)
