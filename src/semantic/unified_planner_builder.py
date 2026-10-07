from src.semantic.unified_planner import UnifiedExecutionPlan


class UnifiedSemanticPlanner:
    """
    Convert UnifiedSemanticProgram into an execution-oriented plan.

    This planner does not execute anything.
    It only translates semantic meaning into ordered intent steps.
    """

    def plan(self, semantic_program):
        plan = UnifiedExecutionPlan()

        self._plan_definitions(plan, semantic_program.definitions)
        self._plan_rules(plan, semantic_program.rules)
        self._plan_bases(plan, semantic_program.bases)
        self._plan_extensions(plan, semantic_program.extensions)
        self._plan_flows(plan, semantic_program.flows)
        self._plan_systems(plan, semantic_program.systems)

        return plan

    def _plan_definitions(self, plan, definitions):
        for definition in definitions:
            name = getattr(definition, "name", str(definition))

            value = getattr(definition, "value", None)
            kind = getattr(definition, "kind", None)

            plan.add(
                "DEFINE",
                name,
                value_kind=kind,
                value=value,
            )

    def _plan_rules(self, plan, rules):
        for rule in rules:
            name = getattr(rule, "name", str(rule))

            condition = getattr(rule, "condition", None)
            effect = getattr(rule, "effect", None)

            plan.add(
                "RULE",
                name,
                condition=condition,
                effect=effect,
            )

    def _plan_bases(self, plan, bases):
        for base in bases:
            name = getattr(base, "name", str(base))
            service = getattr(base, "service", None)
            options = getattr(base, "options", ())

            plan.add(
                "BASE",
                name,
                service=service,
                options=options,
            )

    def _plan_extensions(self, plan, extensions):
        for extension in extensions:
            name = getattr(extension, "name", str(extension))
            base_name = getattr(extension, "base_name", None)
            options = getattr(extension, "options", ())

            plan.add(
                "BASE_EXTENSION",
                name,
                base=base_name,
                options=options,
            )

    def _plan_flows(self, plan, flows):
        for flow in flows:
            name = getattr(flow, "name", str(flow))
            steps = getattr(flow, "steps", ())

            plan.add(
                "FLOW",
                name,
                steps=steps,
            )

    def _plan_systems(self, plan, systems):
        for system in systems:
            name = getattr(system, "name", str(system))
            components = getattr(system, "components", ())

            plan.add(
                "SYSTEM",
                name,
                components=components,
            )
