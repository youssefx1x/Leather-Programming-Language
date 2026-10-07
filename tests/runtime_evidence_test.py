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

validation_errors = IRValidator().validate(ir)

if validation_errors:
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

evidence = ExecutionEvidence(runtime.trace)

if evidence.why_rule_activated("discount") is None:
    print("TEST FAILED: rule activation not explained")
    raise SystemExit(1)

if not evidence.changes("price"):
    print("TEST FAILED: price change not explained")
    raise SystemExit(1)

if abs(state.values["price"] - 135.45) > 0.000001:
    print("TEST FAILED: incorrect final value")
    raise SystemExit(1)

print(evidence.describe())
print()
print("FINAL:")
print(state.values)
print()
print("RUNTIME EVIDENCE TEST PASSED")
