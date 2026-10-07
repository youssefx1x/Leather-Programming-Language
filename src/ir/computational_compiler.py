from src.ir.ir import LTHIR


class ComputationalIRCompiler:
    """Compile Core 0.2 computational semantics into LTH IR."""

    def compile(self, semantic_program):
        ir = LTHIR()

        self._compile_domains(ir, semantic_program.domains)
        self._compile_states(ir, semantic_program.states)
        self._compile_operations(ir, semantic_program.operations)
        self._compile_transitions(ir, semantic_program.transitions)

        return ir

    def _compile_domains(self, ir, domains):
        for domain in domains:
            ir.emit(
                "DOMAIN_BEGIN",
                domain.name,
            )

            ir.emit(
                "DOMAIN_END",
                domain.name,
            )

    def _compile_states(self, ir, states):
        for state in states:
            ir.emit(
                "STATE_BEGIN",
                state.name,
                state.domain,
            )

            for field in state.fields:
                ir.emit(
                    "STATE_FIELD",
                    state.name,
                    field.name,
                    field.semantic_type,
                )

            ir.emit(
                "STATE_END",
                state.name,
            )

    def _compile_operations(self, ir, operations):
        for operation in operations:
            ir.emit(
                "OPERATION_BEGIN",
                operation.name,
            )

            for input_value in operation.inputs:
                ir.emit(
                    "OPERATION_INPUT",
                    operation.name,
                    input_value.name,
                    input_value.semantic_type,
                )

            ir.emit(
                "OPERATION_END",
                operation.name,
            )

    def _compile_transitions(self, ir, transitions):
        for transition in transitions:
            ir.emit(
                "TRANSITION",
                transition.source_state,
                transition.operation,
                transition.target_state,
            )
