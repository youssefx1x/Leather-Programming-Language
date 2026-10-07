from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer
from src.semantic.builder import SemanticBuilder
from src.ir.compiler import IRCompiler
from src.ir.validator import IRValidator
from src.runtime.explainable import ExplainableRuntime


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

runtime = ExplainableRuntime()

state = runtime.execute(
    ir,
    context={
        "customer": {
            "vip": True,
        }
    },
)

print(runtime.trace.describe())
print()
print("FINAL VALUES:")
print(state.values)

if abs(state.values["price"] - 135.45) > 0.000001:
    print("TEST FAILED")
    raise SystemExit(1)

print("EXPLAINABLE RUNTIME TEST PASSED")
