from pathlib import Path

from tools.module_loader import ModuleLoader
from tools.module_composer import (
    ModuleComposer,
    ModuleCompositionError,
)
from src.ir.compiler import IRCompiler
from src.ir.validator import IRValidator
from src.runtime.explainable import ExplainableRuntime


def test_module_composition(tmp_path):
    pricing = tmp_path / "pricing.lth"
    customer = tmp_path / "customer.lth"

    pricing.write_text(
        "price = 150.5\n",
        encoding="utf-8",
    )

    customer.write_text(
        'name = "Leather"\n',
        encoding="utf-8",
    )

    loader = ModuleLoader()

    modules = loader.load_many(
        [pricing, customer]
    )

    composer = ModuleComposer()
    program = composer.compose(modules)

    semantic = composer.analyze(program)

    assert len(
        semantic.definitions
    ) == 2

    ir = IRCompiler().compile(
        semantic
    )

    errors = IRValidator().validate(ir)

    assert errors == []

    runtime = ExplainableRuntime()
    state = runtime.execute(ir)

    assert state.values["price"] == 150.5
    assert state.values["name"] == "Leather"


def test_composed_rule(tmp_path):
    pricing = tmp_path / "pricing.lth"
    rules = tmp_path / "rules.lth"

    pricing.write_text(
        "price = 150.5\n",
        encoding="utf-8",
    )

    rules.write_text(
        "rule discount when customer.vip "
        "-> price *= 0.9\n",
        encoding="utf-8",
    )

    loader = ModuleLoader()

    modules = loader.load_many(
        [pricing, rules]
    )

    composer = ModuleComposer()
    program = composer.compose(modules)
    semantic = composer.analyze(program)

    ir = IRCompiler().compile(
        semantic
    )

    assert IRValidator().validate(ir) == []

    runtime = ExplainableRuntime()

    state = runtime.execute(
        ir,
        context={
            "customer": {
                "vip": True,
            },
        },
    )

    assert abs(
        state.values["price"] - 135.45
    ) < 1e-9


def test_duplicate_definition_current_behavior(tmp_path):
    first = tmp_path / "first.lth"
    second = tmp_path / "second.lth"

    first.write_text(
        "price = 150.5\\n",
        encoding="utf-8",
    )

    second.write_text(
        "price = 200\\n",
        encoding="utf-8",
    )

    loader = ModuleLoader()

    modules = loader.load_many(
        [first, second]
    )

    composer = ModuleComposer()
    program = composer.compose(modules)
    semantic = composer.analyze(program)

    assert len(
        semantic.definitions
    ) == 2

    assert (
        semantic.definitions[-1].name
        == "price"
    )


if __name__ == "__main__":
    test_module_composition(Path("."))
    print("LTH 0.2 COMPOSITION TEST: PASS")
