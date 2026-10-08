from .base_syntax import prepare_source
from .runner import LTH03Runner


class BaseAwareRunner(LTH03Runner):
    def run(self, source, context=None):
        prepared, _ = prepare_source(source)
        return super().run(
            prepared,
            context=context,
        )

    def execute(self, source, context=None):
        return self.run(
            source,
            context=context,
        )
