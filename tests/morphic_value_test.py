from src.runtime.morphic_registry import MorphicRegistry


def test_morphic_value():
    registry = MorphicRegistry()

    value = registry.define(
        "price",
        "number",
        150.5,
    )

    assert value.semantic_type == "number"
    assert value.representation == "native"
    assert value.value == 150.5

    registry.morph(
        "price",
        "compact-number",
        150.5,
    )

    value = registry.get("price")

    assert value.semantic_type == "number"
    assert value.representation == "compact-number"
    assert value.value == 150.5

    registry.morph(
        "price",
        "native",
        135.45,
    )

    value = registry.get("price")

    assert value.semantic_type == "number"
    assert value.value == 135.45

    print(registry.describe())
    print()
    print("MORPHIC VALUE TEST PASSED")


if __name__ == "__main__":
    test_morphic_value()
