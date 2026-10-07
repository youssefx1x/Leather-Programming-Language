from pathlib import Path
import tempfile

from tools.multi_runner import MultiFileRunner
from tools.module_namespace import NamespaceRegistry


def test_final_integration():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)

        core = root / "core.lth"
        rules = root / "rules.lth"
        customer = root / "customer.lth"

        core.write_text(
            'name = "Leather"\n'
            'price = 150.5\n'
            'age = 20\n',
            encoding="utf-8",
        )

        rules.write_text(
            'rule discount when customer.vip -> price *= 0.9\n',
            encoding="utf-8",
        )

        customer.write_text(
            'customer_name = "VIP"\n',
            encoding="utf-8",
        )

        runner = MultiFileRunner()

        result = runner.execute(
            [core, rules, customer],
            context={
                "customer": {
                    "vip": True,
                }
            },
        )

        assert result.values["name"] == "Leather"
        assert result.values["age"] == 20.0
        assert result.values["customer_name"] == "VIP"
        assert abs(result.values["price"] - 135.45) < 1e-9


def test_namespace_isolation():
    registry = NamespaceRegistry()

    pricing = registry.create("pricing")
    customer = registry.create("customer")

    pricing.define("value", 150.5)
    customer.define("value", "VIP")

    assert pricing.get("value") == 150.5
    assert customer.get("value") == "VIP"

    try:
        pricing.get("missing")
        assert False
    except Exception:
        pass


if __name__ == "__main__":
    test_final_integration()
    test_namespace_isolation()
    print("LTH 0.2 FINAL INTEGRATION TEST: PASS")
