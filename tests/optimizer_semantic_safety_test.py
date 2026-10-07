from src.lexer.lexer import Lexer
from src.parser.leather_parser_v3 import LeatherParserV3
from src.semantic.unified_builder import UnifiedSemanticBuilder
from src.semantic.unified_intent import UnifiedIntentContext
from src.semantic.unified_intent_planner import IntentAwareUnifiedPlanner
from src.semantic.resource_envelope import ResourceEnvelope
from src.optimizer.adaptive_optimizer import AdaptiveOptimizer


SOURCE = """price = 150.5

rule discount when customer.vip -> price *= 0.9

base api = service timeout=30 retries=3

secure_api = api with auth=true

flow backup = collect -> compress -> encrypt -> upload

system shop = catalog -> cart -> checkout -> payment -> notify
"""


def semantic_signature(semantic):
    return {
        "definitions": [
            item.name
            for item in semantic.definitions
        ],
        "rules": [
            item.name
            for item in semantic.rules
        ],
        "bases": [
            item.name
            for item in semantic.bases
        ],
        "extensions": [
            item.name
            for item in semantic.extensions
        ],
        "flows": [
            item.name
            for item in semantic.flows
        ],
        "systems": [
            item.name
            for item in semantic.systems
        ],
    }


def test_optimizer_preserves_semantics():
    tokens = Lexer(SOURCE).tokenize()
    program = LeatherParserV3(tokens).parse()

    semantic = UnifiedSemanticBuilder().build(
        program
    )

    before = semantic_signature(semantic)

    intent = UnifiedIntentContext()

    intent.set_decision(
        "execution.mode",
        "streaming",
        "test optimization",
    )

    intent.set_decision(
        "memory.strategy",
        "streaming",
        "test memory optimization",
    )

    envelope = ResourceEnvelope(
        memory_mb=256,
        cpu=4,
    )

    plan = IntentAwareUnifiedPlanner().plan(
        semantic,
        intent,
    )

    AdaptiveOptimizer().optimize(
        plan,
        intent,
        envelope,
    )

    after = semantic_signature(semantic)

    assert before == after

    print("SEMANTIC SIGNATURE PRESERVED")
    print(before)
    print()
    print("OPTIMIZER SEMANTIC SAFETY TEST PASSED")


if __name__ == "__main__":
    test_optimizer_preserves_semantics()
