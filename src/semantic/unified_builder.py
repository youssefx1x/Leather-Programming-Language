from src.semantic.unified_model import UnifiedSemanticProgram
from src.semantic.builder import SemanticBuilder
from src.semantic.base_flow_builder import BaseFlowBuilder
from src.semantic.system_builder import SystemBuilder


class UnifiedSemanticBuilder:
    def __init__(self):
        self.core_builder = SemanticBuilder()
        self.base_flow_builder = BaseFlowBuilder()
        self.system_builder = SystemBuilder()

    def build(self, program):
        unified = UnifiedSemanticProgram()

        core_program = self.core_builder.build(program)
        base_flow_program = self.base_flow_builder.build(program)
        system_program = self.system_builder.build(program)

        unified.definitions.extend(
            getattr(core_program, "definitions", [])
        )

        unified.rules.extend(
            getattr(core_program, "rules", [])
        )

        unified.bases.extend(
            getattr(base_flow_program, "bases", [])
        )

        unified.extensions.extend(
            getattr(base_flow_program, "extensions", [])
        )

        unified.flows.extend(
            getattr(base_flow_program, "flows", [])
        )

        unified.systems.extend(
            getattr(system_program, "systems", [])
        )

        return unified
