from tools.leather import compile_source
from src.runtime.explainable import ExplainableRuntime


SOURCE = '''price = 150.5
rule discount when customer.vip -> price *= 0.9
'''


def test_rule_inactive():
    _, plan, ir = compile_source(SOURCE)

    runtime = ExplainableRuntime()
    state = runtime.execute(
        ir,
        context={
            "customer": {
                "vip": False,
            },
        },
    )

    assert state.values["price"] == 150.5

    trace = runtime.trace.describe()

    assert "discount started" in trace
    assert "customer.vip = false" in trace
    assert "rule discount skipped" in trace


def test_rule_active():
    _, plan, ir = compile_source(SOURCE)

    runtime = ExplainableRuntime()
    state = runtime.execute(
        ir,
        context={
            "customer": {
                "vip": True,
            },
        },
    )

    assert abs(state.values["price"] - 135.45) < 1e-9

    trace = runtime.trace.describe()

    assert "discount started" in trace
    assert "customer.vip = true" in trace
    assert "rule discount activated" in trace
    assert "price: 150.5 -> 135.45000000000002" in trace


if __name__ == "__main__":
    test_rule_inactive()
    test_rule_active()
    print("LTH 0.2 RULE TEST: PASS")
