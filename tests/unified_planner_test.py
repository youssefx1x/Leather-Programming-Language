from src.lexer.lexer import Lexer
from src.parser.leather_parser_v3 import LeatherParserV3
from src.semantic.unified_builder import UnifiedSemanticBuilder
from src.semantic.unified_planner_builder import UnifiedSemanticPlanner


SOURCE = """price = 150.5

rule discount when customer.vip -> price *= 0.9

base api = service timeout=30 retries=3

secure_api = api with auth=true

flow backup = collect -> compress -> encrypt -> upload

system shop = catalog -> cart -> checkout -> payment -> notify
"""


def build_plan():
    tokens = Lexer(SOURCE).tokenize()
    program = LeatherParserV3(tokens).parse()
    semantic = UnifiedSemanticBuilder().build(program)

    planner = UnifiedSemanticPlanner()
    return planner.plan(semantic)


def test_plan():
    plan = build_plan()

    assert len(plan.steps) == 6

    kinds = [step.kind for step in plan.steps]

    assert kinds == [
        "DEFINE",
        "RULE",
        "BASE",
        "BASE_EXTENSION",
        "FLOW",
        "SYSTEM",
    ]

    assert plan.steps[0].name == "price"
    assert plan.steps[1].name == "discount"
    assert plan.steps[2].name == "api"
    assert plan.steps[3].name == "secure_api"
    assert plan.steps[4].name == "backup"
    assert plan.steps[5].name == "shop"

    assert plan.steps[2].details["service"] == "service"
    assert plan.steps[3].details["base"] == "api"
    assert plan.steps[4].details["steps"] == (
        "collect",
        "compress",
        "encrypt",
        "upload",
    )

    print(plan.describe())
    print()
    print("UNIFIED PLANNER TEST PASSED")


if __name__ == "__main__":
    test_plan()
