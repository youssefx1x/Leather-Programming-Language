from pathlib import Path
import tempfile

from tools.multi_runner import MultiFileRunner
from tools.module_namespace import NamespaceRegistry


def test_full_module_integration():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)

        pricing = root / "pricing.lth"
        rules = root / "rules.lth"
        customer = root / "customer.lth"

        pricing.write_text(
            'price = 150.5\n',
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
            [pricing, rules, customer],
            context={
                "customer": {
                    "vip": True,
                }
            },
        )

        assert abs(result.values["price"] - 135.45) < 1e-9
        assert result.values["customer_name"] == "VIP"


def test_namespace_integration():
    registry = NamespaceRegistry()

    pricing = registry.create("pricing")
    customer = registry.create("customer")

    pricing.define("price", 150.5)
    customer.define("name", "VIP")

    assert pricing.get("price") == 150.5
    assert customer.get("name") == "VIP"

    try:
        pricing.get("name")
        assert False
    except Exception:
        pass


if __name__ == "__main__":
    test_full_module_integration()
    test_namespace_integration()

    print("LTH 0.2 MODULE INTEGRATION TEST: PASS")
