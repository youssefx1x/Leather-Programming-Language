from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer
from src.semantic.builder import SemanticBuilder
from src.ir.compiler import IRCompiler
from src.ir.validator import IRValidator
from src.runtime.runtime import LTHRuntime


source = '''price = 150.5
rule discount when customer.vip -> price *= 0.9
'''

tokens = Lexer(source).tokenize()
program = Parser(tokens).parse()

errors = SemanticAnalyzer().analyze(program)

if errors:
    raise SystemExit(1)

semantic = SemanticBuilder().build(program)
ir = IRCompiler().compile(semantic)

if IRValidator().validate(ir):
    raise SystemExit(1)

runtime = LTHRuntime()

state = runtime.execute(
    ir,
    context={
        "customer": {
            "vip": False,
        }
    },
)

print("RUNTIME VALUES:")
print(state.values)

expected = 150.5

if state.values["price"] != expected:
    print("TEST FAILED")
    print(
        f"expected price = {expected}"
    )
    raise SystemExit(1)

print("FALSE CONDITION TEST PASSED")
