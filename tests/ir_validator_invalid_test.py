from src.ir.ir import LTHIR
from src.ir.validator import IRValidator


ir = LTHIR()

ir.emit("RULE_BEGIN", "broken_rule")
ir.emit("EFFECT", "price", "*=", "0.9")
ir.emit("RULE_END", "broken_rule")


errors = IRValidator().validate(ir)

if not errors:
    print("TEST FAILED: invalid IR was accepted")
    raise SystemExit(1)

print("IR INVALID - correctly rejected")

for error in errors:
    print(f"{error.index}: {error.message}")
