from src.lexer.lexer import Lexer
from src.parser.leather_parser_v3 import LeatherParserV3
from src.semantic.unified_builder import UnifiedSemanticBuilder
from src.semantic.unified_intent import UnifiedIntentContext
from src.semantic.unified_intent_planner import IntentAwareUnifiedPlanner


SOURCE = """price = 150.5

rule discount when customer.vip -> price *= 0.9

base api = service timeout=30 retries=3

secure_api = api with auth=true

flow backup = collect -> compress -> encrypt -> upload

system shop = catalog -> cart -> checkout -> payment -> notify
"""


def build_semantic():
    tokens = Lexer(SOURCE).tokenize()
    program = LeatherParserV3(tokens).parse()
    return UnifiedSemanticBuilder().build(program)


def test_intent_aware_planner():
    semantic = build_semantic()

    intent = UnifiedIntentContext()

    intent.set_slot(
        "execution.mode",
        "AUTO",
    )

    intent.set_slot(
        "memory.strategy",
        "streaming",
    )

    intent.set_decision(
        "execution.mode",
        "streaming",
        "AUTO selected streaming execution",
    )

    intent.set_decision(
        "memory.strategy",
        "streaming",
        "explicit memory strategy",
    )

    planner = IntentAwareUnifiedPlanner()
    plan = planner.plan(
        semantic,
        intent,
    )

    flow = next(
        step for step in plan.steps
        if step.kind == "FLOW"
    )

    definition = next(
        step for step in plan.steps
        if step.kind == "DEFINE"
    )

    assert flow.details["execution_mode"] == "streaming"
    assert definition.details["memory_strategy"] == "streaming"

    print(intent.describe())
    print()
    print(plan.describe())
    print()
    print("UNIFIED INTENT PLANNER TEST PASSED")


if __name__ == "__main__":
    test_intent_aware_planner()
