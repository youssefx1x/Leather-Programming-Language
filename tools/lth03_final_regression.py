from pathlib import Path
import runpy
import sys


BASELINE = (
    "tests.lth_03_values_test",
    "tests.lth_03_expression_test",
    "tests.lth_03_logic_test",
    "tests.lth_03_rules_test",
    "tests.lth_03_collections_test",
    "tests.lth_03_integration_test",
    "tests.lth_03_base_test",
    "tests.lth_03_base_extension_test",
    "tests.lth_03_base_validation_test",
    "tests.lth_03_base_language_test",
    "tests.lth_03_base_composition_test",
    "tests.lth_03_base_error_test",
    "tests.lth_03_flow_test",
    "tests.lth_03_flow_composition_test",
    "tests.lth_03_system_test",
    "tests.lth_03_system_error_test",
    "tests.lth_03_ir_test",
)


def main():
    root = Path(__file__).resolve().parents[1]

    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    for module in BASELINE:
        relative = Path(
            module.replace(".", "/") + ".py"
        )
        runpy.run_path(
            str(root / relative),
            run_name="__main__",
        )

    print(
        "LTH 0.3 FINAL REGRESSION: "
        f"{len(BASELINE)}/{len(BASELINE)} PASS"
    )


if __name__ == "__main__":
    main()
