from src.ir.ir import LTHIR
from src.runtime.runtime import LTHRuntime


ir = LTHIR()

ir.emit(
    "DEFINE",
    "price",
    "number",
    "150.5",
)

ir.emit(
    "RULE_BEGIN",
    "broken_rule",
)

ir.emit(
    "CHECK_MEMBER",
    "customer",
    "vip",
)

ir.emit("IF_TRUE")

ir.emit(
    "EFFECT",
    "unknown_price",
    "*=",
    "0.9",
)

ir.emit(
    "RULE_END",
    "broken_rule",
)


runtime = LTHRuntime()

try:
    runtime.execute(
        ir,
        context={
            "customer": {
                "vip": True,
            }
        },
    )

except Exception as error:
    print("RUNTIME ERROR - correctly rejected")
    print(error)
else:
    print("TEST FAILED: invalid runtime operation was accepted")
    raise SystemExit(1)
