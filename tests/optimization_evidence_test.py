from src.lexer.lexer import Lexer
from src.parser.leather_parser_v3 import LeatherParserV3

from src.semantic.unified_builder import (
    UnifiedSemanticBuilder,
)

from src.semantic.unified_intent_planner import (
    IntentAwareUnifiedPlanner,
)

from src.semantic.resource_envelope import (
    ResourceEnvelope,
)

from src.semantic.resource_intent import (
    ResourceIntentResolver,
)

from src.optimizer.adaptive_optimizer import (
    AdaptiveOptimizer,
)

from src.ir.optimized_compiler import (
    OptimizedIRCompiler,
)


SOURCE = """price = 150.5

rule discount when customer.vip -> price *= 0.9

base api = service timeout=30 retries=3

secure_api = api with auth=true

flow backup = collect -> compress -> encrypt -> upload

system shop = catalog -> cart -> checkout -> payment -> notify
"""


def test_optimization_evidence():
    tokens = Lexer(SOURCE).tokenize()
    program = LeatherParserV3(tokens).parse()

    semantic = UnifiedSemanticBuilder().build(
        program
    )

    envelope = ResourceEnvelope(
        memory_mb=256,
        time_ms=500,
        cpu=4,
        gpu=1,
    )

    intent = ResourceIntentResolver().resolve(
        envelope
    )

    plan = IntentAwareUnifiedPlanner().plan(
        semantic,
        intent,
    )

    optimized = AdaptiveOptimizer().optimize(
        plan,
        intent,
        envelope,
    )

    _, evidence = OptimizedIRCompiler().compile(
        semantic,
        optimized,
    )

    backup = evidence.why("backup")

    assert backup

    assert any(
        event.strategy == "latency"
        for event in backup
    )

    gpu = evidence.find(
        strategy="gpu"
    )

    assert gpu

    memory = evidence.find(
        strategy="memory-streaming"
    )

    assert memory

    print(evidence.describe())
    print()
    print("OPTIMIZATION EVIDENCE TEST PASSED")


if __name__ == "__main__":
    test_optimization_evidence()
