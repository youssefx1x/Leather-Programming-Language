from src.lexer.lexer import Lexer
from src.parser.leather_parser_v2 import LeatherParserV2
from src.semantic.base_flow_builder import BaseFlowBuilder
from src.semantic.base_flow_meaning import BaseFlowMeaning
from src.ir.base_flow_compiler import BaseFlowIRCompiler
from src.ir.base_flow_validator import BaseFlowValidator
from src.runtime.base_flow import BaseFlowRuntime


source = '''base api = service timeout=30 retries=3
secure_api = api with auth=true

flow backup = collect -> compress -> encrypt -> upload
'''

tokens = Lexer(source).tokenize()

program = LeatherParserV2(tokens).parse()

semantic = BaseFlowBuilder().build(program)

meaning = BaseFlowMeaning()

for base in semantic.bases:
    meaning.add_base(base)

for extension in semantic.extensions:
    meaning.add_extension(extension)

for flow in semantic.flows:
    meaning.add_flow(flow)

print(meaning.describe())
print()

ir = BaseFlowIRCompiler().compile(
    semantic
)

print(ir.describe())
print()

errors = BaseFlowValidator().validate(ir)

if errors:
    print("BASE/FLOW IR INVALID")

    for error in errors:
        print(
            f"{error.index}: {error.message}"
        )

    raise SystemExit(1)

runtime = BaseFlowRuntime()

state = runtime.execute(ir)

print("BASES:")
print(state.bases)
print()

print("FLOWS:")
print(state.flows)
print()

if "api" not in state.bases:
    raise SystemExit(1)

if "secure_api" not in state.bases:
    raise SystemExit(1)

if state.bases["secure_api"]["options"]["auth"] is not True:
    raise SystemExit(1)

if state.flows["backup"] != [
    "collect",
    "compress",
    "encrypt",
    "upload",
]:
    raise SystemExit(1)

print("BASE/FLOW TEST PASSED")
