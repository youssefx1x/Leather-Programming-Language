from src.ir.ir import LTHIR


class IRCompiler:
    def compile(self, semantic_program):
        ir = LTHIR()

        for definition in semantic_program.definitions:
            ir.emit(
                "DEFINE",
                definition.name,
                definition.value.kind,
                definition.value.value,
            )

        for rule in semantic_program.rules:
            ir.emit(
                "RULE_BEGIN",
                rule.name,
            )

            ir.emit(
                "CHECK_MEMBER",
                rule.condition.object_name,
                rule.condition.member_name,
            )

            ir.emit(
                "IF_TRUE",
            )

            ir.emit(
                "EFFECT",
                rule.effect.target,
                rule.effect.operator,
                rule.effect.value.value,
            )

            ir.emit(
                "RULE_END",
                rule.name,
            )

        return ir
