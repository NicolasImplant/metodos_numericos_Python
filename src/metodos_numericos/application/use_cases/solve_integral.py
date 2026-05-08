from __future__ import annotations

import logging
from pathlib import Path

from ...domain.models.numerical_result import IntegralResult
from ...domain.ports.solvers import IntegralSolverPort
from ...domain.ports.visualizer import VisualizerPort
from ...infrastructure.problems.integral_registry import INTEGRAL_PROBLEMS

logger = logging.getLogger(__name__)


class SolveIntegralUseCase:
    def __init__(self, solver: IntegralSolverPort, visualizer: VisualizerPort) -> None:
        self._solver = solver
        self._visualizer = visualizer

    def execute(
        self,
        problem_id: int,
        n_steps: int,
        save_path: Path | None = None,
    ) -> IntegralResult:
        problem = INTEGRAL_PROBLEMS.get(problem_id)
        if problem is None:
            raise KeyError(f"No integral problem with id={problem_id}. Valid: {list(INTEGRAL_PROBLEMS)}")

        logger.info("Solving '%s' with %s (%d steps)", problem.name, self._solver.method_name, n_steps)
        result = self._solver.solve(problem, n_steps)

        if problem.analytical_value is not None:
            pct_error = abs(result.area - problem.analytical_value) / problem.analytical_value * 100
            logger.info("Numerical result: %.6f | Analytical: %.6f | Error: %.4f%%",
                        result.area, problem.analytical_value, pct_error)
        else:
            logger.info("Numerical result: %.6f", result.area)

        self._visualizer.plot_integral(result, save_path=save_path)
        return result
