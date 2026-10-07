from src.lexer.lexer import Lexer
from src.parser.leather_parser_v3 import LeatherParserV3
from src.semantic.unified_builder import UnifiedSemanticBuilder
from src.semantic.resource_envelope import ResourceEnvelope
from src.semantic.resource_intent import ResourceIntentResolver
from src.semantic.unified_intent_planner import UnifiedIntentPlanner
from src.optimizer.adaptive_optimizer import AdaptiveOptimizer
from src.ir.optimized_compiler import OptimizedIRCompiler
from src.runtime.morphing_runtime import MorphingRuntime
from src.runtime.observation import RuntimeObservation


SOURCE = """
price = 150.5
rule discount when customer.vip -> price *= 0.9
base api = service timeout=30 retries=3
secure_api = api with auth=true
flow backup = collect -> compress -> encrypt -> upload
system shop = catalog -> cart -> checkout -> payment -> notify
"""


def build_runtime():
    tokens = Lexer(SOURCE).tokenize()
    parser = LeatherParserV3(tokens)
    program = parser.parse()

    semantic = UnifiedSemanticBuilder().build(program)

    envelope = ResourceEnvelope(
        memory_mb=1024,
        time_ms=500,
        cpu=4,
        gpu=1,
    )

    intent = ResourceIntentResolver().resolve(
        envelope
    )

    plan = UnifiedIntentPlanner().plan(
        semantic,
        intent,
    )

    optimized = AdaptiveOptimizer().optimize(
        plan,
        intent=intent,
        envelope=envelope,
    )

    ir, evidence = OptimizedIRCompiler().compile(
        semantic,
        optimized_plan=optimized,
    )

    return ir


def test_morphing_runtime():
    ir = build_runtime()

    runtime = MorphingRuntime()

    runtime.execute(
        ir,
        context={
            "customer": {
                "vip": True,
            }
        },
    )

    assert runtime.state.values["price"] == 135.45000000000002

    initial = runtime.strategy_for("backup")

    assert initial == "latency"

    decision = runtime.observe_and_morph(
        "backup",
        RuntimeObservation(
            memory_mb=128,
        ),
    )

    assert decision is not None
    assert decision.new_strategy == "streaming"

    assert runtime.strategy_for("backup") == "streaming"

    assert len(runtime.morphing_evidence.events) == 1

    print("INITIAL STRATEGY:")
    print(initial)

    print("MORPHED STRATEGY:")
    print(runtime.strategy_for("backup"))

    print("MORPHING EVIDENCE:")
    print(runtime.morphing_evidence.describe())

    print("FINAL VALUES:")
    print(runtime.state.values)

    print("MORPHING RUNTIME TEST PASSED")


if __name__ == "__main__":
    test_morphing_runtime()
