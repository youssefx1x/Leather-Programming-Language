from src.ir.ir import LTHIR


class BaseFlowIRCompiler:
    def compile(self, semantic_program):
        ir = LTHIR()

        for base in semantic_program.bases:
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

        for extension in semantic_program.extensions:
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

        for flow in semantic_program.flows:
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

        return ir
