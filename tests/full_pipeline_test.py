from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer
from src.semantic.builder import SemanticBuilder
from src.semantic.planner import SemanticPlanner
from src.ir.compiler import IRCompiler
from src.ir.validator import IRValidator
from src.runtime.explainable import ExplainableRuntime
from src.runtime.evidence import ExecutionEvidence


source = '''price = 150.5
rule discount when customer.vip -> price *= 0.9
'''

tokens = Lexer(source).tokenize()

program = Parser(tokens).parse()

semantic_errors = SemanticAnalyzer().analyze(program)

if semantic_errors:
    print("SEMANTIC FAILURE")
    raise SystemExit(1)

semantic_program = SemanticBuilder().build(program)

plan = SemanticPlanner().plan(
    semantic_program
)

if not plan.steps:
    print("PLANNER FAILURE")
    raise SystemExit(1)

ir = IRCompiler().compile(
    semantic_program
)

validation_errors = IRValidator().validate(ir)

if validation_errors:
    print("IR VALIDATION FAILURE")

    for error in validation_errors:
        print(
            f"{error.index}: {error.message}"
        )

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

evidence = ExecutionEvidence(
    runtime.trace
)

if abs(
    state.values["price"] - 135.45
) > 0.000001:
    print("RUNTIME FAILURE")
    raise SystemExit(1)

if evidence.why_rule_activated(
    "discount"
) is None:
    print("EVIDENCE FAILURE")
    raise SystemExit(1)

print("FULL LTH PIPELINE")
print("=================")
print("Lexer:             PASS")
print("Parser:            PASS")
print("Semantic:          PASS")
print("Planner:           PASS")
print("IR Compiler:       PASS")
print("IR Validator:      PASS")
print("Runtime:           PASS")
print("Evidence:          PASS")
print()
print("FINAL VALUES:")
print(state.values)
print()
print("FULL PIPELINE TEST PASSED")
