from __future__ import annotations

import logging
from pathlib import Path

from ...domain.models.numerical_result import ODEResult
from ...domain.ports.solvers import ODESolverPort
from ...domain.ports.visualizer import VisualizerPort
from ...infrastructure.problems.ode_registry import ODE_PROBLEMS

logger = logging.getLogger(__name__)


class SolveODEUseCase:
    def __init__(self, solver: ODESolverPort, visualizer: VisualizerPort) -> None:
        self._solver = solver
        self._visualizer = visualizer

    def execute(
        self,
        problem_id: int,
        n_steps: int,
        save_path: Path | None = None,
    ) -> ODEResult:
        problem = ODE_PROBLEMS.get(problem_id)
        if problem is None:
            raise KeyError(f"No ODE problem with id={problem_id}. Valid: {list(ODE_PROBLEMS)}")

        logger.info("Solving '%s' with %s (%d steps)", problem.name, self._solver.method_name, n_steps)
        result = self._solver.solve(problem, n_steps)
        logger.info("Integration complete. Shape: %s", result.states.shape)

        self._visualizer.plot_ode(result, save_path=save_path)
        return result
