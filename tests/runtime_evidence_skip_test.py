from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer
from src.semantic.builder import SemanticBuilder
from src.ir.compiler import IRCompiler
from src.ir.validator import IRValidator
from src.runtime.explainable import ExplainableRuntime
from src.runtime.evidence import ExecutionEvidence


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
            "vip": False,
        }
    },
)

evidence = ExecutionEvidence(runtime.trace)

if state.values["price"] != 150.5:
    print("TEST FAILED: effect executed unexpectedly")
    raise SystemExit(1)

if not evidence.find("SKIP"):
    print("TEST FAILED: skip evidence missing")
    raise SystemExit(1)

if evidence.changes("price"):
    print("TEST FAILED: unexpected change evidence")
    raise SystemExit(1)

print(evidence.describe())
print()
print("SKIP EVIDENCE TEST PASSED")
