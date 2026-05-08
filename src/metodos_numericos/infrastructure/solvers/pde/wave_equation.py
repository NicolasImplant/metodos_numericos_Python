from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from ....domain.models.numerical_result import PDEResult
from ....domain.models.problems import PDEProblem
from ....domain.ports.solvers import PDESolverPort


class WaveEquationSolver(PDESolverPort):
    """
    Explicit finite-difference solver for the 1D wave equation:
        d²u/dt² = c² * d²u/dx²
    Uses the standard three-level scheme. Stable when c*dt/dx ≤ 1.
    """

    @property
    def method_name(self) -> str:
        return "Finite Difference Wave"

    def solve(self, problem: PDEProblem) -> PDEResult:
        c = problem.num_spatial_points
        f = problem.num_time_steps
        x = np.linspace(0.0, problem.spatial_length, c)
        t = np.linspace(0.0, problem.total_time, f)
        dx = x[1] - x[0]
        dt = t[1] - t[0]
        cfl = (problem.wave_speed * dt / dx) ** 2

        M: NDArray[np.float64] = np.zeros((f, c))
        M[0, :] = problem.initial_condition(x)
        M[1, :] = M[0, :]  # zero initial velocity
        M[:, 0] = problem.boundary_conditions[0]
        M[:, -1] = problem.boundary_conditions[1]

        for n in range(1, f - 1):
            for m in range(1, c - 1):
                M[n + 1, m] = (
                    2 * M[n, m]
                    - M[n - 1, m]
                    + cfl * (M[n, m - 1] - 2 * M[n, m] + M[n, m + 1])
                )

        return PDEResult(
            spatial_grid=x,
            time_grid=t,
            solution_matrix=M,
            method_name=self.method_name,
            problem_name=problem.name,
            metadata={"cfl_squared": cfl},
        )
