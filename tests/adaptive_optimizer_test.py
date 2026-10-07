from src.lexer.lexer import Lexer
from src.parser.leather_parser_v3 import LeatherParserV3
from src.semantic.unified_builder import UnifiedSemanticBuilder
from src.semantic.unified_intent_planner import IntentAwareUnifiedPlanner
from src.semantic.resource_envelope import ResourceEnvelope
from src.semantic.resource_intent import ResourceIntentResolver
from src.optimizer.adaptive_optimizer import AdaptiveOptimizer


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


def test_adaptive_optimizer():
    semantic = build_semantic()

    envelope = ResourceEnvelope(
        memory_mb=256,
        time_ms=500,
        cpu=4,
        gpu=1,
    )

    intent = ResourceIntentResolver().resolve(
        envelope
    )

    planner = IntentAwareUnifiedPlanner()

    plan = planner.plan(
        semantic,
        intent,
    )

    optimized = AdaptiveOptimizer().optimize(
        plan,
        intent,
        envelope,
    )

    flow = next(
        step for step in optimized.plan.steps
        if step.kind == "FLOW"
    )

    definition = next(
        step for step in optimized.plan.steps
        if step.kind == "DEFINE"
    )

    system = next(
        step for step in optimized.plan.steps
        if step.kind == "SYSTEM"
    )

    assert flow.details["optimization"] == "latency"
    assert flow.details["scheduling"] == "eager"
    assert flow.details["compute_target"] == "gpu"

    assert (
        definition.details["memory_optimization"]
        == "streaming"
    )

    assert (
        system.details["scheduling"]
        == "parallel-capable"
    )

    assert len(optimized.report.decisions) >= 4

    print(optimized.describe())
    print()
    print("ADAPTIVE OPTIMIZER TEST PASSED")


if __name__ == "__main__":
    test_adaptive_optimizer()
