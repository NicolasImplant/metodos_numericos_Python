from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from ....domain.models.numerical_result import ODEResult
from ....domain.models.problems import ODEProblem
from ....domain.ports.solvers import ODESolverPort


class VerletSolver(ODESolverPort):
    """
    Störmer-Verlet algorithm for second-order systems.

    Expects state = [position, velocity]. The system function must return
    [velocity, acceleration(t, position, velocity)].
    """

    @property
    def method_name(self) -> str:
        return "Verlet"

    def solve(self, problem: ODEProblem, n_steps: int) -> ODEResult:
        dt = (problem.t_end - problem.t_start) / (n_steps - 1)
        t = np.linspace(problem.t_start, problem.t_end, n_steps)
        n_states = len(problem.initial_conditions)
        states: NDArray[np.float64] = np.zeros((n_steps, n_states))
        states[0] = problem.initial_conditions

        # Bootstrap first step with Euler to have two positions for Verlet
        deriv0 = problem.system(t[0], states[0])
        accel0 = deriv0[1]  # acceleration is the second component
        # x1 = x0 + v0*dt + 0.5*a0*dt²
        states[1, 0] = states[0, 0] + states[0, 1] * dt + 0.5 * accel0 * dt**2
        states[1, 1] = states[0, 1] + accel0 * dt

        for i in range(1, n_steps - 1):
            deriv = problem.system(t[i], states[i])
            accel = deriv[1]
            # Classic Verlet position update (needs previous position)
            states[i + 1, 0] = 2 * states[i, 0] - states[i - 1, 0] + accel * dt**2
            # Velocity from central difference
            if i > 0:
                states[i, 1] = (states[i + 1, 0] - states[i - 1, 0]) / (2 * dt)

        return ODEResult(
            time=t,
            states=states,
            state_labels=tuple(problem.state_labels),
            method_name=self.method_name,
            problem_name=problem.name,
        )
