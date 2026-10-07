from pathlib import Path

from tools.module_loader import ModuleLoader
from tools.module_composer import ModuleComposer
from tools.leather import compile_source
from src.ir.compiler import IRCompiler
from src.runtime.explainable import ExplainableRuntime


class MultiFileRunnerError(Exception):
    pass


class MultiFileRunner:
    def __init__(self):
        self.loader = ModuleLoader()
        self.composer = ModuleComposer()

    def load_modules(self, paths):
        return self.loader.load_many(paths)

    def compose(self, paths):
        modules = self.load_modules(paths)
        return self.composer.compose(modules)

    def execute(self, paths, context=None):
        program = self.compose(paths)

        try:
            semantic = self.composer.analyze(program)
        except Exception as error:
            raise MultiFileRunnerError(str(error)) from error

        compiler = IRCompiler()
        ir = compiler.compile(semantic)

        runtime = ExplainableRuntime()
        return runtime.execute(ir, context=context)
