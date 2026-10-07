from pathlib import Path

from tools.module_loader import (
    ModuleLoader,
    ModuleLoadError,
)


def test_load_module(tmp_path):
    path = tmp_path / "pricing.lth"

    path.write_text(
        "price = 150.5\n",
        encoding="utf-8",
    )

    loader = ModuleLoader()
    module = loader.load(path)

    assert module.path == path.resolve()
    assert module.source == "price = 150.5\n"


def test_module_cache(tmp_path):
    path = tmp_path / "pricing.lth"

    path.write_text(
        "price = 150.5\n",
        encoding="utf-8",
    )

    loader = ModuleLoader()

    first = loader.load(path)
    second = loader.load(path)

    assert first is second


def test_missing_module(tmp_path):
    loader = ModuleLoader()

    try:
        loader.load(
            tmp_path / "missing.lth"
        )
        assert False
    except ModuleLoadError as error:
        assert "module not found" in str(error)


def test_invalid_module_type(tmp_path):
    path = tmp_path / "pricing.txt"

    path.write_text(
        "price = 150.5\n",
        encoding="utf-8",
    )

    loader = ModuleLoader()

    try:
        loader.load(path)
        assert False
    except ModuleLoadError as error:
        assert "unsupported module type" in str(error)


def test_load_many(tmp_path):
    first = tmp_path / "pricing.lth"
    second = tmp_path / "customer.lth"

    first.write_text(
        "price = 150.5\n",
        encoding="utf-8",
    )

    second.write_text(
        'name = "Leather"\n',
        encoding="utf-8",
    )

    loader = ModuleLoader()

    modules = loader.load_many(
        [first, second]
    )

    assert len(modules) == 2
    assert modules[0].source == "price = 150.5\n"
    assert modules[1].source == 'name = "Leather"\n'


if __name__ == "__main__":
    test_load_module(Path("."))
    print("LTH 0.2 MODULE TEST: PASS")
