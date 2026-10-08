from .compiler import LTH05Compiler
from .optimizer import optimize
from .vm import VirtualMachine


class LTH05Runner:
    def __init__(self, step_limit=1_000_000):
        self.compiler = LTH05Compiler()
        self.vm = VirtualMachine(step_limit=step_limit)

    def compile(self, source):
        code = self.compiler.compile_source(source)
        optimized, report = optimize(code)
        return optimized, report

    def run(self, source, context=None, trace=False):
        code, report = self.compile(source)
        result = self.vm.run(
            code,
            context=context,
            trace=trace,
        )
        result.values["_lth05"] = {
            "optimization": report,
            "profile": result.profile.summary(),
        }
        return result
