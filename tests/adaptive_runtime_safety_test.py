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

from src.runtime.unified import (
    UnifiedRuntime,
)

from src.runtime.adaptive import (
    AdaptiveRuntime,
)


SOURCE = """price = 150.5

rule discount when customer.vip -> price *= 0.9

base api = service timeout=30 retries=3

secure_api = api with auth=true

flow backup = collect -> compress -> encrypt -> upload

system shop = catalog -> cart -> checkout -> payment -> notify
"""


def build_ir():
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

    ir, _ = OptimizedIRCompiler().compile(
        semantic,
        optimized,
    )

    return ir


def test_runtime_equivalence():
    ir = build_ir()

    context = {
        "customer": {
            "vip": True,
        }
    }

    normal = UnifiedRuntime()

    normal.execute(
        ir,
        context=context,
    )

    adaptive = AdaptiveRuntime()

    adaptive.execute(
        ir,
        context=context,
    )

    assert (
        normal.state.values
        == adaptive.state.values
    )

    print("NORMAL RUNTIME:")
    print(normal.state.values)

    print()
    print("ADAPTIVE RUNTIME:")
    print(adaptive.state.values)

    print()
    print("RUNTIME EQUIVALENCE TEST PASSED")


if __name__ == "__main__":
    test_runtime_equivalence()
