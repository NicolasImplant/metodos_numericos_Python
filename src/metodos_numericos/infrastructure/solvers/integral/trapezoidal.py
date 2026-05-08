from __future__ import annotations

import numpy as np

from ....domain.models.numerical_result import IntegralResult
from ....domain.models.problems import IntegralProblem
from ....domain.ports.solvers import IntegralSolverPort


class TrapezoidalSolver(IntegralSolverPort):
    """Composite trapezoidal rule."""

    @property
    def method_name(self) -> str:
        return "Trapezoidal"

    def solve(self, problem: IntegralProblem, n_steps: int) -> IntegralResult:
        history: list[float] = []
        for n in range(2, n_steps + 1):
            history.append(self._trap(problem, n))

        errors = [
            abs((history[i] - history[i - 1]) / history[i])
            for i in range(1, len(history))
            if history[i] != 0.0
        ]

        return IntegralResult(
            area=history[-1],
            convergence_history=tuple(history),
            error_history=tuple(errors),
            method_name=self.method_name,
            problem_name=problem.name,
        )

    def _trap(self, problem: IntegralProblem, n: int) -> float:
        a, b = problem.lower_bound, problem.upper_bound
        h = (b - a) / (n - 1)
        x = a
        area = 0.0
        for _ in range(n):
            area += (h / 2) * (problem.integrand(x) + problem.integrand(x + h))
            x += h
        return area
