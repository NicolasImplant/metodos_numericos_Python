"""ODE solver tests — verify accuracy against analytical solution dy/dt = -y."""
from __future__ import annotations

import numpy as np
import pytest

from metodos_numericos.domain.models.problems import ODEProblem
from metodos_numericos.infrastructure.solvers.ode.runge_kutta4 import RungeKutta4Solver
from metodos_numericos.infrastructure.solvers.ode.heun import HeunSolver
from metodos_numericos.infrastructure.solvers.ode.midpoint import MidpointSolver


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
