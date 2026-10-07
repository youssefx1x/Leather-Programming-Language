from src.lexer.lexer import Lexer
from src.parser.leather_parser_v3 import LeatherParserV3

from src.semantic.builder import SemanticBuilder
from src.semantic.base_flow_builder import BaseFlowBuilder
from src.semantic.system_builder import SystemBuilder

from src.ir.compiler import IRCompiler
from src.ir.base_flow_compiler import BaseFlowIRCompiler
from src.ir.system_compiler import SystemIRCompiler

from src.ir.validator import IRValidator
from src.ir.base_flow_validator import BaseFlowValidator
from src.ir.system_validator import SystemValidator

from src.runtime.runtime import LTHRuntime
from src.runtime.base_flow import BaseFlowRuntime
from src.runtime.system import SystemRuntime


source = """price = 150.5

rule discount when customer.vip -> price *= 0.9

base api = service timeout=30 retries=3

secure_api = api with auth=true

flow backup = collect -> compress -> encrypt -> upload

system shop = catalog -> cart -> checkout -> payment -> notify
"""


print("LTH 0.1 INTEGRATION")
print("====================")


# --------------------------------------------------
# Lexer
# --------------------------------------------------

tokens = Lexer(source).tokenize()

print("Lexer: PASS")


# --------------------------------------------------
# Parser
# --------------------------------------------------

program = LeatherParserV3(tokens).parse()

print("Parser: PASS")


# --------------------------------------------------
# Semantic layers
# --------------------------------------------------

core_semantic = SemanticBuilder().build(program)
base_flow_semantic = BaseFlowBuilder().build(program)
system_semantic = SystemBuilder().build(program)

print("Semantic: PASS")


# --------------------------------------------------
# Core IR
# --------------------------------------------------

core_ir = IRCompiler().compile(core_semantic)

core_errors = IRValidator().validate(core_ir)

if core_errors:
    print("Core IR: FAIL")

    for error in core_errors:
        print(error)

    raise SystemExit(1)

print("Core IR: PASS")


# --------------------------------------------------
# Base / Flow IR
# --------------------------------------------------

base_flow_ir = BaseFlowIRCompiler().compile(
    base_flow_semantic
)

base_flow_errors = BaseFlowValidator().validate(
    base_flow_ir
)

if base_flow_errors:
    print("Base/Flow IR: FAIL")

    for error in base_flow_errors:
        print(error)

    raise SystemExit(1)

print("Base/Flow IR: PASS")


# --------------------------------------------------
# System IR
# --------------------------------------------------

system_ir = SystemIRCompiler().compile(
    system_semantic
)

system_errors = SystemValidator().validate(
    system_ir
)

if system_errors:
    print("System IR: FAIL")

    for error in system_errors:
        print(error)

    raise SystemExit(1)

print("System IR: PASS")


# --------------------------------------------------
# Core Runtime
# --------------------------------------------------

runtime = LTHRuntime()

# Integration context for the rule condition.
state = runtime.execute(
    core_ir,
    context={
        "customer": {
            "vip": True,
        },
    },
)

if abs(state.values["price"] - 135.45) > 0.000001:
    print("Core Runtime: FAIL")
    print(state.values)
    raise SystemExit(1)

print("Core Runtime: PASS")


# --------------------------------------------------
# Base / Flow Runtime
# --------------------------------------------------

base_flow_runtime = BaseFlowRuntime()

base_flow_state = base_flow_runtime.execute(
    base_flow_ir
)

if "api" not in base_flow_state.bases:
    raise SystemExit(1)

if "secure_api" not in base_flow_state.bases:
    raise SystemExit(1)

if base_flow_state.bases["secure_api"]["options"]["auth"] is not True:
    raise SystemExit(1)

if base_flow_state.flows["backup"] != [
    "collect",
    "compress",
    "encrypt",
    "upload",
]:
    raise SystemExit(1)

print("Base/Flow Runtime: PASS")


# --------------------------------------------------
# System Runtime
# --------------------------------------------------

system_runtime = SystemRuntime()

system_state = system_runtime.execute(
    system_ir
)

components = [
    component["name"]
    for component in system_state.systems["shop"]["components"]
]

expected = [
    "catalog",
    "cart",
    "checkout",
    "payment",
    "notify",
]

if components != expected:
    print("System Runtime: FAIL")
    print(components)
    raise SystemExit(1)

print("System Runtime: PASS")


# --------------------------------------------------
# Final
# --------------------------------------------------

print()
print("FINAL VALUES:")
print(state.values)

print()
print("BASES:")
print(base_flow_state.bases)

print()
print("FLOWS:")
print(base_flow_state.flows)

print()
print("SYSTEMS:")
print(system_state.systems)

print()
print("LTH 0.1 INTEGRATION TEST PASSED")
