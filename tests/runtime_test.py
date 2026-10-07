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

analyzer = SemanticAnalyzer()
errors = analyzer.analyze(program)

if errors:
    for error in errors:
        print(error.message)
    raise SystemExit(1)

semantic = SemanticBuilder().build(program)
ir = IRCompiler().compile(semantic)

validation_errors = IRValidator().validate(ir)

if validation_errors:
    for error in validation_errors:
        print(error.message)
    raise SystemExit(1)

runtime = LTHRuntime()

state = runtime.execute(
    ir,
    context={
        "customer": {
            "vip": True,
        }
    },
)

print("RUNTIME VALUES:")
print(state.values)

expected = 135.45

if abs(state.values["price"] - expected) > 0.000001:
    print("TEST FAILED")
    print(
        f"expected price = {expected}"
    )
    raise SystemExit(1)

print("RUNTIME TEST PASSED")
