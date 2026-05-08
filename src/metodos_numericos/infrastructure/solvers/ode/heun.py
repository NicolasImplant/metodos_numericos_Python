from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from ....domain.models.numerical_result import ODEResult
from ....domain.models.problems import ODEProblem
from ....domain.ports.solvers import ODESolverPort


class HeunSolver(ODESolverPort):
    """Heun's method (explicit trapezoidal / RK2)."""

    @property
    def method_name(self) -> str:
        return "Heun"

    def solve(self, problem: ODEProblem, n_steps: int) -> ODEResult:
        h = (problem.t_end - problem.t_start) / (n_steps - 1)
        t = np.linspace(problem.t_start, problem.t_end, n_steps)
        n_states = len(problem.initial_conditions)
        states: NDArray[np.float64] = np.zeros((n_steps, n_states))
        states[0] = problem.initial_conditions

        for i in range(n_steps - 1):
            y = states[i]
            k1 = problem.system(t[i], y)
            y_pred = y + h * k1
            k2 = problem.system(t[i] + h, y_pred)
            states[i + 1] = y + (h / 2) * (k1 + k2)

        return ODEResult(
            time=t,
            states=states,
            state_labels=tuple(problem.state_labels),
            method_name=self.method_name,
            problem_name=problem.name,
        )
