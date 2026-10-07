from src.ir.ir import LTHIR
from src.ir.unified_value import UnifiedValueNormalizer


class UnifiedIRCompiler:
    def __init__(self):
        self.normalizer = UnifiedValueNormalizer()

    def compile(self, semantic_program):
        ir = LTHIR()

        self._compile_definitions(ir, semantic_program.definitions)
        self._compile_rules(ir, semantic_program.rules)
        self._compile_bases(ir, semantic_program.bases)
        self._compile_extensions(ir, semantic_program.extensions)
        self._compile_flows(ir, semantic_program.flows)
        self._compile_systems(ir, semantic_program.systems)

        return ir

    def _compile_definitions(self, ir, definitions):
        for definition in definitions:
            name = definition.name
            value = definition.value

            kind = self.normalizer.kind(value)
            value = self.normalizer.normalize(value)

            ir.emit(
                "DEFINE",
                name,
                kind,
                value,
            )

    def _compile_rules(self, ir, rules):
        for rule in rules:
            ir.emit(
                "RULE_BEGIN",
                rule.name,
            )

            condition = rule.condition
            ir.emit(
                "CHECK_MEMBER",
                condition.object_name,
                condition.member_name,
            )

            ir.emit("IF_TRUE")

            effect = rule.effect
            ir.emit(
                "EFFECT",
                effect.target,
                effect.operator,
                self.normalizer.normalize(effect.value),
            )

            ir.emit(
                "RULE_END",
                rule.name,
            )

    def _compile_bases(self, ir, bases):
        for base in bases:
            ir.emit(
                "BASE_BEGIN",
                base.name,
                base.service,
            )

            for option in base.options:
                ir.emit(
                    "BASE_OPTION",
                    base.name,
                    option.name,
                    option.value,
                )

            ir.emit(
                "BASE_END",
                base.name,
            )

    def _compile_extensions(self, ir, extensions):
        for extension in extensions:
            ir.emit(
                "EXTEND_BASE",
                extension.name,
                extension.base_name,
            )

            for option in extension.options:
                ir.emit(
                    "EXTENSION_OPTION",
                    extension.name,
                    option.name,
                    option.value,
                )

    def _compile_flows(self, ir, flows):
        for flow in flows:
            ir.emit(
                "FLOW_BEGIN",
                flow.name,
            )

            for step in flow.steps:
                ir.emit(
                    "FLOW_STEP",
                    flow.name,
                    step,
                )

            ir.emit(
                "FLOW_END",
                flow.name,
            )

    def _compile_systems(self, ir, systems):
        for system in systems:
            ir.emit(
                "SYSTEM_BEGIN",
                system.name,
            )

            for index, component in enumerate(system.components):
                ir.emit(
                    "SYSTEM_COMPONENT",
                    system.name,
                    index,
                    component,
                )

            ir.emit(
                "SYSTEM_END",
                system.name,
            )
