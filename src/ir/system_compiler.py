from src.ir.ir import LTHIR


class SystemIRCompiler:
    def compile(self, semantic_program):
        ir = LTHIR()

        for system in semantic_program.systems:
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

        return ir
