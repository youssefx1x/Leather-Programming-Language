from src.lth03.ir_bridge import LTH03SemanticBridge


source = """
base Product {
    price = 100
    active = true
}

flow subtotal {
    total = item.price * quantity
}

system Shop {
    use flow subtotal
}

run system Shop
"""

bridge = LTH03SemanticBridge()

analysis = bridge.analyze(source)

assert "Product" in analysis["base_names"]
assert "subtotal" in analysis["flow_names"]
assert "Shop" in analysis["system_names"]

ir = bridge.compile(source)

ops = tuple(
    instruction.op
    for instruction in ir.instructions
)

assert "BASE_DEFINE" in ops
assert "FLOW_DEFINE" in ops
assert "SYSTEM_DEFINE" in ops
assert "AST_PROGRAM" in ops
assert len(ir.source_hash) == 64

print("LTH 0.3-I SEMANTIC IR BRIDGE: PASS")
