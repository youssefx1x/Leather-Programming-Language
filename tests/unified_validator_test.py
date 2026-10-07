from src.lexer.lexer import Lexer
from src.parser.leather_parser_v3 import LeatherParserV3
from src.semantic.unified_builder import UnifiedSemanticBuilder
from src.ir.unified_compiler import UnifiedIRCompiler
from src.ir.unified_validator import UnifiedIRValidator
from src.ir.ir import LTHIR


SOURCE = """price = 150.5

rule discount when customer.vip -> price *= 0.9

base api = service timeout=30 retries=3

secure_api = api with auth=true

flow backup = collect -> compress -> encrypt -> upload

system shop = catalog -> cart -> checkout -> payment -> notify
"""


def compile_source(source):
    tokens = Lexer(source).tokenize()
    program = LeatherParserV3(tokens).parse()
    semantic = UnifiedSemanticBuilder().build(program)
    return UnifiedIRCompiler().compile(semantic)


def test_valid_unified_ir():
    ir = compile_source(SOURCE)

    validator = UnifiedIRValidator()

    assert validator.is_valid(ir), validator.describe(ir)

    print("VALID UNIFIED IR:")
    print(validator.describe(ir))


def test_invalid_unknown_opcode():
    ir = LTHIR()
    ir.emit("DEFINE", "price", "number", 150.5)
    ir.emit("MAGIC_OPCODE", "x")

    validator = UnifiedIRValidator()
    errors = validator.validate(ir)

    assert errors
    assert "unknown opcode 'MAGIC_OPCODE'" in errors[0]

    print("INVALID UNKNOWN OPCODE:")
    print(validator.describe(ir))


def test_invalid_rule():
    ir = LTHIR()
    ir.emit("RULE_BEGIN", "broken")
    ir.emit("RULE_END", "broken")

    validator = UnifiedIRValidator()
    errors = validator.validate(ir)

    assert errors
    assert any("rule has no condition" in error for error in errors)
    assert any("rule has no effect" in error for error in errors)

    print("INVALID RULE:")
    print(validator.describe(ir))


def test_invalid_flow():
    ir = LTHIR()
    ir.emit("FLOW_STEP", "backup", "compress")

    validator = UnifiedIRValidator()
    errors = validator.validate(ir)

    assert errors
    assert "FLOW_STEP outside flow" in errors[0]

    print("INVALID FLOW:")
    print(validator.describe(ir))


def test_invalid_system():
    ir = LTHIR()
    ir.emit("SYSTEM_END", "shop")

    validator = UnifiedIRValidator()
    errors = validator.validate(ir)

    assert errors
    assert "SYSTEM_END without SYSTEM_BEGIN" in errors[0]

    print("INVALID SYSTEM:")
    print(validator.describe(ir))


if __name__ == "__main__":
    test_valid_unified_ir()
    test_invalid_unknown_opcode()
    test_invalid_rule()
    test_invalid_flow()
    test_invalid_system()

    print()
    print("UNIFIED IR VALIDATOR TEST PASSED")
