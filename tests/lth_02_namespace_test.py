from tools.module_namespace import (
    ModuleNamespace,
    NamespaceRegistry,
    ModuleNamespaceError,
)


def test_module_symbols_are_isolated():
    pricing = ModuleNamespace("pricing")
    customer = ModuleNamespace("customer")

    pricing.define("price", 150.5)
    customer.define("price", 200)

    assert pricing.get("price") == 150.5
    assert customer.get("price") == 200


def test_duplicate_symbol_inside_module():
    pricing = ModuleNamespace("pricing")

    pricing.define("price", 150.5)

    try:
        pricing.define("price", 200)
        assert False
    except ModuleNamespaceError as error:
        assert "duplicate symbol 'price'" in str(error)


def test_unknown_symbol():
    pricing = ModuleNamespace("pricing")

    try:
        pricing.get("price")
        assert False
    except ModuleNamespaceError as error:
        assert "unknown symbol 'price'" in str(error)


def test_registry():
    registry = NamespaceRegistry()

    pricing = registry.create("pricing")

    assert registry.get("pricing") is pricing


def test_duplicate_module():
    registry = NamespaceRegistry()

    registry.create("pricing")

    try:
        registry.create("pricing")
        assert False
    except ModuleNamespaceError as error:
        assert "already exists" in str(error)


if __name__ == "__main__":
    test_module_symbols_are_isolated()
    test_duplicate_symbol_inside_module()
    test_unknown_symbol()
    test_registry()
    test_duplicate_module()

    print("LTH 0.2 NAMESPACE TEST: PASS")
