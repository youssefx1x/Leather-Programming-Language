from src.lth03.base import BaseError, BaseRegistry
from src.lth03.base_syntax import BaseSyntaxError, prepare_source


registry = BaseRegistry()

try:
    registry.define(
        "A",
        {"x": 1},
        extends="A",
    )
except BaseError:
    pass
else:
    raise AssertionError(
        "self inheritance must fail"
    )

registry.define(
    "B",
    {"x": 1},
    extends="C",
)

registry.define(
    "C",
    {"y": 2},
    extends="B",
)

try:
    registry.validate()
except BaseError:
    pass
else:
    raise AssertionError(
        "inheritance cycle must fail"
    )

try:
    prepare_source(
        """
        base Product {
            price = 100
        }

        item = Product({"missing": 5})
        """
    )
except BaseSyntaxError:
    pass
else:
    raise AssertionError(
        "unknown override must fail"
    )

try:
    prepare_source(
        """
        base Broken {
            price
        }
        """
    )
except BaseSyntaxError:
    pass
else:
    raise AssertionError(
        "invalid base field syntax must fail"
    )

print("LTH 0.3-F BASE ERRORS: PASS")
