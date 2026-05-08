from __future__ import annotations

import logging
from pathlib import Path

from ...domain.models.numerical_result import PDEResult
from ...domain.ports.solvers import PDESolverPort
from ...domain.ports.visualizer import VisualizerPort
from ...infrastructure.problems.pde_registry import PDE_PROBLEMS

logger = logging.getLogger(__name__)


class SolvePDEUseCase:
    def __init__(self, solver: PDESolverPort, visualizer: VisualizerPort) -> None:
        self._solver = solver
        self._visualizer = visualizer

    def execute(
        self,
        problem_id: int,
        save_path: Path | None = None,
    ) -> PDEResult:
        problem = PDE_PROBLEMS.get(problem_id)
        if problem is None:
            raise KeyError(f"No PDE problem with id={problem_id}. Valid: {list(PDE_PROBLEMS)}")

        logger.info("Solving '%s' with %s", problem.name, self._solver.method_name)
        result = self._solver.solve(problem)
        logger.info("PDE solved. Grid: %dx%d", *result.solution_matrix.shape)

        self._visualizer.plot_pde(result, save_path=save_path)
        return result
