"""Integral solver tests — verify convergence to known analytical values."""
from __future__ import annotations

import numpy as np
import pytest

from metodos_numericos.domain.models.problems import IntegralProblem
from metodos_numericos.infrastructure.solvers.integral.simpson import SimpsonSolver
from metodos_numericos.infrastructure.solvers.integral.trapezoidal import TrapezoidalSolver
from metodos_numericos.infrastructure.solvers.integral.midpoint_rect import MidpointRectSolver


class TestSimpsonSolver:
    def test_sine_converges_to_2(self, sine_integral: IntegralProblem) -> None:
        result = SimpsonSolver().solve(sine_integral, n_steps=100)
        assert abs(result.area - 2.0) < 1e-6

    def test_semicircle_converges_to_pi_over_2(self, semicircle_integral: IntegralProblem) -> None:
        result = SimpsonSolver().solve(semicircle_integral, n_steps=200)
        assert abs(result.area - np.pi / 2) < 1e-3

    def test_result_has_convergence_history(self, sine_integral: IntegralProblem) -> None:
        result = SimpsonSolver().solve(sine_integral, n_steps=20)
        assert len(result.convergence_history) == 19  # range(2, 21) → 19 entries

    def test_method_name(self) -> None:
        assert "Simpson" in SimpsonSolver().method_name


class TestTrapezoidalSolver:
    def test_sine_converges_to_2(self, sine_integral: IntegralProblem) -> None:
        result = TrapezoidalSolver().solve(sine_integral, n_steps=1000)
        assert abs(result.area - 2.0) < 1e-4

    def test_method_name(self) -> None:
        assert "Trapezoidal" in TrapezoidalSolver().method_name


class TestMidpointRectSolver:
    def test_sine_converges(self, sine_integral: IntegralProblem) -> None:
        result = MidpointRectSolver().solve(sine_integral, n_steps=500)
        assert abs(result.area - 2.0) < 1e-2

    def test_method_name(self) -> None:
        assert "Midpoint" in MidpointRectSolver().method_name
