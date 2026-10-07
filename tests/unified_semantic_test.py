from src.lexer.lexer import Lexer
from src.parser.leather_parser_v3 import LeatherParserV3
from src.semantic.unified_builder import UnifiedSemanticBuilder
from src.semantic.unified_meaning import UnifiedMeaningBuilder


SOURCE = """price = 150.5

rule discount when customer.vip -> price *= 0.9

base api = service timeout=30 retries=3

secure_api = api with auth=true

flow backup = collect -> compress -> encrypt -> upload

system shop = catalog -> cart -> checkout -> payment -> notify
"""


def main():
    tokens = Lexer(SOURCE).tokenize()

    parser = LeatherParserV3(tokens)
    program = parser.parse()

    semantic = UnifiedSemanticBuilder().build(program)

    counts = semantic.counts()

    expected = {
        "definitions": 1,
        "rules": 1,
        "bases": 1,
        "extensions": 1,
        "flows": 1,
        "systems": 1,
        "domains": 0,
        "states": 0,
        "operations": 0,
        "transitions": 0,
    }

    if counts != expected:
        raise SystemExit(
            f"UNIFIED SEMANTIC FAIL: {counts}"
        )

    graph = UnifiedMeaningBuilder().build(semantic)

    if len(graph.nodes) != 6:
        raise SystemExit(
            f"UNIFIED MEANING FAIL: expected 6 nodes, "
            f"got {len(graph.nodes)}"
        )

    print(graph.describe())
    print()
    print("COUNTS:")
    print(counts)
    print()
    print("UNIFIED SEMANTIC TEST PASSED")


if __name__ == "__main__":
    main()
