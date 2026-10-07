from src.lexer.lexer import Lexer
from src.parser.system_parser import SystemParser
from src.semantic.system_builder import SystemBuilder
from src.semantic.system_meaning import SystemMeaning
from src.ir.system_compiler import SystemIRCompiler
from src.ir.system_validator import SystemValidator
from src.runtime.system import SystemRuntime


source = """system shop = catalog -> cart -> checkout -> payment -> notify
"""


tokens = Lexer(source).tokenize()

program = SystemParser(tokens).parse()

semantic = SystemBuilder().build(program)


meaning = SystemMeaning()

for system in semantic.systems:
    meaning.add_system(system)

print(meaning.describe())
print()


ir = SystemIRCompiler().compile(semantic)

print(ir.describe())
print()


errors = SystemValidator().validate(ir)

if errors:
    print("SYSTEM IR INVALID")

    for error in errors:
        print(f"{error.index}: {error.message}")

    raise SystemExit(1)


runtime = SystemRuntime()

state = runtime.execute(ir)

print("SYSTEMS:")
print(state.systems)
print()


expected = [
    "catalog",
    "cart",
    "checkout",
    "payment",
    "notify",
]

actual = [
    component["name"]
    for component in state.systems["shop"]["components"]
]


if actual != expected:
    print("SYSTEM COMPONENT TEST FAILED")
    print("Expected:", expected)
    print("Actual:", actual)
    raise SystemExit(1)


print("SYSTEM TEST PASSED")
