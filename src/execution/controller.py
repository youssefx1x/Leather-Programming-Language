from dataclasses import dataclass

from src.execution.benchmark import ExecutionBenchmark
from src.execution.budget import ExecutionBudget
from src.execution.portfolio import (
    ExecutionStrategyPortfolio,
)
from src.execution.model import ExecutionWorkload
from src.execution.plan import ExecutionPlan
from src.execution.plan_validator import (
    ExecutionPlanValidator,
)
from src.integration.sea_bridge import (
    LEATHERSEABridge,
)
from src.semantic.execution_intent import (
    ExecutionIntent,
)
from src.sea_objective import SEAOptimizationObjective


@dataclass(frozen=True)
class AdaptiveExecutionResult:
    workload: ExecutionWorkload
    intent: ExecutionIntent
    plan: ExecutionPlan
    benchmark: object
    sea_certificate: object

    @property
    def valid(self):
        return (
            self.plan.valid
            and self.benchmark.valid
            and self.sea_certificate.valid
        )

    def summary(self):
        return {
            "workload": self.workload.name,
            "strategy":
                self.plan.strategy.value,
            "plan_valid": self.plan.valid,
            "benchmark":
                self.benchmark.summary(),
            "sea_certificate":
                self.sea_certificate.summary(),
            "valid": self.valid,
        }


class AdaptiveExecutionController:
    def __init__(self):
        self.portfolio = (
            ExecutionStrategyPortfolio()
        )
        self.validator = (
            ExecutionPlanValidator()
        )
        self.benchmark = ExecutionBenchmark()

    def run(
        self,
        workload,
        source_function,
        optimized_function,
        intent=None,
        budget=None,
    ):
        intent = (
            intent
            if intent is not None
            else ExecutionIntent()
        )

        budget = (
            budget
            if budget is not None
            else ExecutionBudget()
        )

        _, plan = self.portfolio.build(
            workload=workload,
            budget=budget,
            intent=intent,
        )

        if plan is None:
            raise ValueError(
                "no execution strategy satisfies constraints"
            )

        if not self.validator.validate(plan):
            raise ValueError(
                "execution plan validation failed"
            )

        benchmark = self.benchmark.compare(
            source_function=source_function,
            optimized_function=optimized_function,
            semantics_preserved=(
                intent.preserve_semantics
            ),
        )

        source_cost = workload.strategy_cost(
            "direct"
        )

        optimized_cost = plan.estimated_cost

        objective = SEAOptimizationObjective(
            time=1.0,
            memory=0.60,
            states=0.75,
            branching=0.40,
            depth=0.20,
            precision=0.05,
            interactions=0.50,
        )

        certificate = (
            LEATHERSEABridge.certificate(
                name=(
                    "adaptive:"
                    + plan.strategy.value
                ),
                source_cost=source_cost,
                target_cost=optimized_cost,
                semantics_preserved=(
                    intent.preserve_semantics
                ),
                objective=objective,
                allow_tradeoff=True,
            )
        )

        return AdaptiveExecutionResult(
            workload=workload,
            intent=intent,
            plan=plan,
            benchmark=benchmark,
            sea_certificate=certificate,
        )
