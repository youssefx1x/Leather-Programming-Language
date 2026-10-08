from .base_runner import BaseAwareRunner
from .flow_syntax import (
    extract_flows,
    expand_flow_runs,
)
from .system_syntax import (
    extract_systems,
    expand_system_runs,
)


class LTH03FinalRunner(BaseAwareRunner):
    def prepare(self, source):
        source_without_flows, flows = extract_flows(
            source
        )

        source_without_systems, systems = extract_systems(
            source_without_flows
        )

        expanded = expand_system_runs(
            source_without_systems,
            systems,
            flows,
        )

        expanded = expand_flow_runs(
            expanded,
            flows,
        )

        return expanded, flows, systems

    def run(self, source, context=None):
        prepared, _, _ = self.prepare(source)

        return super().run(
            prepared,
            context=context,
        )

    def execute(self, source, context=None):
        return self.run(
            source,
            context=context,
        )
