"""ODE solver tests — verify accuracy against analytical solution dy/dt = -y."""
from __future__ import annotations

import numpy as np
import pytest

from metodos_numericos.domain.models.problems import ODEProblem
from metodos_numericos.infrastructure.solvers.ode.runge_kutta4 import RungeKutta4Solver
from metodos_numericos.infrastructure.solvers.ode.heun import HeunSolver
from metodos_numericos.infrastructure.solvers.ode.midpoint import MidpointSolver
from metodos_numericos.infrastructure.solvers.ode.double_pendulum_verlet import DoublePendulumVerletSolver
from metodos_numericos.infrastructure.problems.ode_registry import ODE_PROBLEMS


TOLERANCE = 1e-3  # relative tolerance at t=5


def analytical(t: float) -> float:
    return float(np.exp(-t))


class TestRungeKutta4Solver:
    def test_exponential_decay(self, simple_ode: ODEProblem) -> None:
        result = RungeKutta4Solver().solve(simple_ode, n_steps=1000)
        y_final = result.states[-1, 0]
        expected = analytical(5.0)
        assert abs(y_final - expected) / expected < TOLERANCE

    def test_output_shape(self, simple_ode: ODEProblem) -> None:
        result = RungeKutta4Solver().solve(simple_ode, n_steps=500)
        assert result.states.shape == (500, 1)
        assert result.time.shape == (500,)

    def test_method_name(self) -> None:
        assert "Runge-Kutta" in RungeKutta4Solver().method_name

    def test_state_labels_preserved(self, simple_ode: ODEProblem) -> None:
        result = RungeKutta4Solver().solve(simple_ode, n_steps=100)
        assert result.state_labels == ("y",)


class TestHeunSolver:
    def test_exponential_decay(self, simple_ode: ODEProblem) -> None:
        result = HeunSolver().solve(simple_ode, n_steps=5000)
        y_final = result.states[-1, 0]
        expected = analytical(5.0)
        assert abs(y_final - expected) / expected < TOLERANCE

    def test_method_name(self) -> None:
        assert "Heun" in HeunSolver().method_name


class TestMidpointSolver:
    def test_exponential_decay(self, simple_ode: ODEProblem) -> None:
        result = MidpointSolver().solve(simple_ode, n_steps=5000)
        y_final = result.states[-1, 0]
        expected = analytical(5.0)
        assert abs(y_final - expected) / expected < TOLERANCE

    def test_method_name(self) -> None:
        assert "Midpoint" in MidpointSolver().method_name


class TestDoublePendulumVerletSolver:
    @pytest.fixture()
    def double_pendulum_problem(self) -> ODEProblem:
        return ODE_PROBLEMS[8]

    def test_output_shape(self, double_pendulum_problem: ODEProblem) -> None:
        result = DoublePendulumVerletSolver().solve(double_pendulum_problem, n_steps=1000)
        assert result.states.shape == (1000, 4)
        assert result.time.shape == (1000,)

    def test_method_name(self) -> None:
        assert "Verlet" in DoublePendulumVerletSolver().method_name

    def test_metadata_keys(self, double_pendulum_problem: ODEProblem) -> None:
        result = DoublePendulumVerletSolver().solve(double_pendulum_problem, n_steps=500)
        for key in ("x1", "y1", "x2", "y2", "energy"):
            assert key in result.metadata
            assert result.metadata[key].shape == (500,)

    def test_cartesian_rod_lengths(self, double_pendulum_problem: ODEProblem) -> None:
        """L1 and L2 are both 1 m — verify the rod-length constraint is satisfied."""
        result = DoublePendulumVerletSolver().solve(double_pendulum_problem, n_steps=2000)
        x1, y1 = result.metadata["x1"], result.metadata["y1"]
        x2, y2 = result.metadata["x2"], result.metadata["y2"]
        rod1 = np.sqrt(x1**2 + y1**2)
        rod2 = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        np.testing.assert_allclose(rod1, 1.0, atol=1e-10)
        np.testing.assert_allclose(rod2, 1.0, atol=1e-10)

    def test_energy_near_conservation(self, double_pendulum_problem: ODEProblem) -> None:
        """Velocity Verlet must keep absolute energy drift bounded over 30 s.

        Initial conditions give E0≈0 (bobs horizontal, no velocity), so relative
        drift is ill-defined. We compare against the characteristic energy scale
        E_ref = (m1+m2)*g*L1 + m2*g*L2 ≈ 29.43 J (maximum potential energy range).
        """
        result = DoublePendulumVerletSolver().solve(double_pendulum_problem, n_steps=30_000)
        energy = result.metadata["energy"]
        e_ref = (1.0 + 1.0) * 9.81 * 1.0 + 1.0 * 9.81 * 1.0  # 29.43 J
        abs_drift = np.abs(energy - energy[0])
        # The velocity-dependent coupling introduces O(h) secular drift; 10 % over 30 s
        # is expected and acceptable for this near-symplectic scheme.
        assert float(abs_drift.max()) < 0.10 * e_ref

    def test_initial_conditions_preserved(self, double_pendulum_problem: ODEProblem) -> None:
        result = DoublePendulumVerletSolver().solve(double_pendulum_problem, n_steps=500)
        np.testing.assert_allclose(result.states[0], double_pendulum_problem.initial_conditions)
