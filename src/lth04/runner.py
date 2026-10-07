import time

from .cache import CompilationCache
from .compiler import BytecodeCompiler
from .model import ExecutionStats
from .optimizer import BytecodeOptimizer
from .vm import BytecodeVM


class LTH04Runner:
    def __init__(
        self,
        use_cache=True,
        cache=None,
    ):
        self.compiler = BytecodeCompiler()
        self.optimizer = BytecodeOptimizer()
        self.vm = BytecodeVM()
        self.use_cache = use_cache
        self.cache = cache or CompilationCache()

    def compile(self, source):
        program = None

        if self.use_cache:
            program = self.cache.get(
                self._cache_key(source)
            )

        if program is None:
            program = self.compiler.compile(
                source
            )
            program = self.optimizer.optimize(
                program
            )
            self.optimizer.validate(
                program
            )

            if self.use_cache:
                self.cache.put(
                    self._cache_key(source),
                    program,
                )

        return program

    def _cache_key(self, source):
        return source

    def run(
        self,
        source,
        context=None,
        trace=False,
    ):
        started = time.perf_counter()

        before_hits = self.cache.hits
        program = self.compile(source)
        cache_hit = (
            self.use_cache
            and self.cache.hits > before_hits
        )

        state, stats = self.vm.execute(
            program,
            context=context,
            trace=trace,
        )

        stats.cache_hit = cache_hit
        stats.elapsed = (
            time.perf_counter() - started
        )

        return state

    def execute(
        self,
        source,
        context=None,
        trace=False,
    ):
        return self.vm.execute(
            self.compile(source),
            context=context,
            trace=trace,
        )

    def explain(
        self,
        source,
        context=None,
    ):
        state, stats = self.execute(
            source,
            context=context,
            trace=True,
        )

        return {
            "values": dict(
                state.values
            ),
            "cache_hit": stats.cache_hit,
            "instruction_count": (
                stats.instruction_count
            ),
            "elapsed": stats.elapsed,
            "trace": list(stats.trace),
        }
