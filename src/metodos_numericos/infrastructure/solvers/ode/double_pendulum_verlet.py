from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from ....domain.models.numerical_result import ODEResult
from ....domain.models.problems import ODEProblem
from ....domain.ports.solvers import ODESolverPort

# Physical constants baked into this solver (same as the problem definition)
_M1: float = 1.0
_M2: float = 1.0
_L1: float = 1.0
_L2: float = 1.0
_G: float = 9.81


class DoublePendulumVerletSolver(ODESolverPort):
    """
    Velocity-Verlet (leapfrog) integrator for the double pendulum.

    The double pendulum is a Hamiltonian system with 2 degrees of freedom.
    Its acceleration depends on both position and velocity (coupling terms
    omega_1^2 and omega_2^2 appear), so the classic 3-point Stormer-Verlet
    cannot be applied directly. The leapfrog variant handles velocity-dependent
    forces by evaluating the acceleration at a half-step velocity estimate:

        omega_half = omega_n + (h/2) * alpha(theta_n, omega_n)
        theta_{n+1} = theta_n + h * omega_half
        alpha_{n+1} = alpha(theta_{n+1}, omega_half)     ← O(h) approx in omega
        omega_{n+1} = omega_half + (h/2) * alpha_{n+1}

    The O(h) approximation in the velocity argument of alpha introduces an
    O(h^3) error per step in the velocity update, preserving the overall
    second-order accuracy of the scheme. For Hamiltonian systems with
    velocity-independent forces the method is exactly symplectic; here it
    is near-symplectic with bounded energy drift O(h^2) over long times.

    State vector: [theta_1, theta_2, omega_1, omega_2]
    System must return: [omega_1, omega_2, alpha_1, alpha_2]
    """

    @property
    def method_name(self) -> str:
        return "Velocity Verlet (Leapfrog)"

    def solve(self, problem: ODEProblem, n_steps: int) -> ODEResult:
        h = (problem.t_end - problem.t_start) / (n_steps - 1)
        t = np.linspace(problem.t_start, problem.t_end, n_steps)

        states: NDArray[np.float64] = np.zeros((n_steps, 4))
        states[0] = problem.initial_conditions

        theta = problem.initial_conditions[:2].copy()
        omega = problem.initial_conditions[2:].copy()
        alpha = self._acceleration(problem, t[0], theta, omega)

        for i in range(n_steps - 1):
            omega_half = omega + 0.5 * h * alpha
            theta_new = theta + h * omega_half
            alpha_new = self._acceleration(problem, t[i + 1], theta_new, omega_half)
            omega_new = omega_half + 0.5 * h * alpha_new

            theta, omega, alpha = theta_new, omega_new, alpha_new
            states[i + 1] = np.concatenate([theta, omega])

        return ODEResult(
            time=t,
            states=states,
            state_labels=tuple(problem.state_labels),
            method_name=self.method_name,
            problem_name=problem.name,
            metadata=self._compute_metadata(states),
        )

    @staticmethod
    def _acceleration(
        problem: ODEProblem,
        t_val: float,
        theta: NDArray[np.float64],
        omega: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        state = np.concatenate([theta, omega])
        return problem.system(t_val, state)[2:]

    @staticmethod
    def _compute_metadata(states: NDArray[np.float64]) -> dict[str, NDArray[np.float64]]:
        """Convert angular states to Cartesian coordinates and compute total energy."""
        th1, th2 = states[:, 0], states[:, 1]
        om1, om2 = states[:, 2], states[:, 3]

        # Cartesian positions
        x1 = _L1 * np.sin(th1)
        y1 = -_L1 * np.cos(th1)
        x2 = x1 + _L2 * np.sin(th2)
        y2 = y1 - _L2 * np.cos(th2)

        # Lagrangian energy: T + V
        T = (
            0.5 * (_M1 + _M2) * _L1**2 * om1**2
            + 0.5 * _M2 * _L2**2 * om2**2
            + _M2 * _L1 * _L2 * om1 * om2 * np.cos(th1 - th2)
        )
        V = -(_M1 + _M2) * _G * _L1 * np.cos(th1) - _M2 * _G * _L2 * np.cos(th2)

        energy = T + V
        return {
            "x1": x1, "y1": y1,
            "x2": x2, "y2": y2,
            "energy": energy,
        }
