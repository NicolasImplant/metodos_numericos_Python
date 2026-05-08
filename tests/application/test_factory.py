"""Factory creates the correct concrete solver for each method enum."""
from __future__ import annotations

import pytest

from metodos_numericos.application.factories.solver_factory import SolverFactory
from metodos_numericos.infrastructure.config.settings import IntegralMethod, ODEMethod, PDEMethod
from metodos_numericos.infrastructure.solvers.integral.simpson import SimpsonSolver
from metodos_numericos.infrastructure.solvers.integral.trapezoidal import TrapezoidalSolver
from metodos_numericos.infrastructure.solvers.ode.runge_kutta4 import RungeKutta4Solver
from metodos_numericos.infrastructure.solvers.ode.heun import HeunSolver
from metodos_numericos.infrastructure.solvers.ode.midpoint import MidpointSolver
from metodos_numericos.infrastructure.solvers.ode.verlet import VerletSolver
from metodos_numericos.infrastructure.solvers.ode.double_pendulum_verlet import DoublePendulumVerletSolver
from metodos_numericos.infrastructure.solvers.pde.explicit_euler_heat import ExplicitEulerHeatSolver
from metodos_numericos.infrastructure.solvers.pde.wave_equation import WaveEquationSolver


@pytest.mark.parametrize("method,expected_type", [
    (IntegralMethod.SIMPSON, SimpsonSolver),
    (IntegralMethod.TRAPEZOIDAL, TrapezoidalSolver),
])
def test_integral_factory(method: IntegralMethod, expected_type: type) -> None:
    solver = SolverFactory.create_integral_solver(method)
    assert isinstance(solver, expected_type)


@pytest.mark.parametrize("method,expected_type", [
    (ODEMethod.RUNGE_KUTTA4, RungeKutta4Solver),
    (ODEMethod.HEUN, HeunSolver),
    (ODEMethod.MIDPOINT, MidpointSolver),
    (ODEMethod.VERLET, VerletSolver),
    (ODEMethod.DOUBLE_PENDULUM_VERLET, DoublePendulumVerletSolver),
])
def test_ode_factory(method: ODEMethod, expected_type: type) -> None:
    solver = SolverFactory.create_ode_solver(method)
    assert isinstance(solver, expected_type)


@pytest.mark.parametrize("method,expected_type", [
    (PDEMethod.EXPLICIT_EULER_HEAT, ExplicitEulerHeatSolver),
    (PDEMethod.WAVE_EQUATION, WaveEquationSolver),
])
def test_pde_factory(method: PDEMethod, expected_type: type) -> None:
    solver = SolverFactory.create_pde_solver(method)
    assert isinstance(solver, expected_type)
