import time

from src.lth03.runner import LTH03Runner

from .model import ExecutionStats


class BytecodeVM:
    def __init__(self):
        self.runtime = LTH03Runner()

    def execute(
        self,
        program,
        context=None,
        trace=False,
    ):
        stats = ExecutionStats(
            instruction_count=len(
                program.instructions
            )
        )

        start = time.perf_counter()
        state = None

        for index, instruction in enumerate(
            program.instructions
        ):
            if trace:
                stats.trace.append(
                    {
                        "pc": index,
                        "op": instruction.op,
                    }
                )

            if instruction.op == "EXECUTE":
                state = self.runtime.run(
                    instruction.arg,
                    context=context,
                )

            elif instruction.op == "HALT":
                break

        stats.elapsed = (
            time.perf_counter() - start
        )

        if state is None:
            raise RuntimeError(
                "bytecode halted without execution"
            )

        return state, stats
