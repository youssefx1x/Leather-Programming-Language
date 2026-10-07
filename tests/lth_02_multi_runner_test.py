from pathlib import Path
import tempfile

from tools.multi_runner import MultiFileRunner


def test_multi_file_execution():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)

        first = root / "data.lth"
        second = root / "rules.lth"

        first.write_text(
            'price = 150.5\n'
            'name = "Leather"\n',
            encoding="utf-8",
        )

        second.write_text(
            'rule discount when customer.vip -> price *= 0.9\n',
            encoding="utf-8",
        )

        runner = MultiFileRunner()

        result = runner.execute(
            [first, second],
            context={
                "customer": {
                    "vip": True,
                }
            },
        )

        assert abs(result.values["price"] - 135.45) < 1e-9
        assert result.values["name"] == "Leather"


if __name__ == "__main__":
    test_multi_file_execution()
    print("LTH 0.2 MULTI-RUNNER TEST: PASS")
