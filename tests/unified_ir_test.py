from src.lexer.lexer import Lexer
from src.parser.leather_parser_v3 import LeatherParserV3
from src.semantic.unified_builder import UnifiedSemanticBuilder
from src.ir.unified_compiler import UnifiedIRCompiler


SOURCE = """price = 150.5

rule discount when customer.vip -> price *= 0.9

base api = service timeout=30 retries=3

secure_api = api with auth=true

flow backup = collect -> compress -> encrypt -> upload

system shop = catalog -> cart -> checkout -> payment -> notify
"""


def main():
    tokens = Lexer(SOURCE).tokenize()

    program = LeatherParserV3(tokens).parse()

    semantic = UnifiedSemanticBuilder().build(program)

    ir = UnifiedIRCompiler().compile(semantic)

    print(ir.describe())

    expected = [
        "DEFINE",
        "RULE_BEGIN",
        "CHECK_MEMBER",
        "IF_TRUE",
        "EFFECT",
        "RULE_END",
        "BASE_BEGIN",
        "BASE_OPTION",
        "BASE_OPTION",
        "BASE_END",
        "EXTEND_BASE",
        "EXTENSION_OPTION",
        "FLOW_BEGIN",
        "FLOW_STEP",
        "FLOW_STEP",
        "FLOW_STEP",
        "FLOW_STEP",
        "FLOW_END",
        "SYSTEM_BEGIN",
        "SYSTEM_COMPONENT",
        "SYSTEM_COMPONENT",
        "SYSTEM_COMPONENT",
        "SYSTEM_COMPONENT",
        "SYSTEM_COMPONENT",
        "SYSTEM_END",
    ]

    actual = [
        instruction.opcode
        for instruction in ir.instructions
    ]

    if actual != expected:
        raise SystemExit(
            "UNIFIED IR FAIL\n"
            f"Expected: {expected}\n"
            f"Actual:   {actual}"
        )

    print()
    print("UNIFIED IR TEST PASSED")


if __name__ == "__main__":
    main()
