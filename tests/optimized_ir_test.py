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

from src.ir.optimization_validator import (
    OptimizationIRValidator,
)


SOURCE = """price = 150.5

rule discount when customer.vip -> price *= 0.9

base api = service timeout=30 retries=3

secure_api = api with auth=true

flow backup = collect -> compress -> encrypt -> upload

system shop = catalog -> cart -> checkout -> payment -> notify
"""


def build():
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

    ir, evidence = OptimizedIRCompiler().compile(
        semantic,
        optimized,
    )

    return ir, evidence


def test_optimized_ir():
    ir, evidence = build()

    unified_validator = OptimizationIRValidator()

    assert unified_validator.is_valid(ir), (
        unified_validator.describe(ir)
    )

    hints = [
        instruction
        for instruction in ir.instructions
        if instruction.opcode == "OPTIMIZATION_HINT"
    ]

    assert len(hints) >= 4

    strategies = [
        instruction.operands[2]
        for instruction in hints
    ]

    assert any(
        "latency" in strategy
        for strategy in strategies
    )

    assert any(
        "memory:streaming" in strategy
        for strategy in strategies
    )

    assert any(
        "compute:gpu" in strategy
        for strategy in strategies
    )

    assert len(evidence.events) >= 4

    print(ir.describe())
    print()
    print(evidence.describe())
    print()
    print(
        unified_validator.describe(ir)
    )
    print()
    print("OPTIMIZED IR TEST PASSED")


if __name__ == "__main__":
    test_optimized_ir()
