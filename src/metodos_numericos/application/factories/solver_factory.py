from __future__ import annotations

from ...domain.ports.solvers import IntegralSolverPort, ODESolverPort, PDESolverPort
from ...infrastructure.config.settings import IntegralMethod, ODEMethod, PDEMethod
from ...infrastructure.solvers.integral.midpoint_rect import MidpointRectSolver
from ...infrastructure.solvers.integral.simpson import SimpsonSolver
from ...infrastructure.solvers.integral.trapezoidal import TrapezoidalSolver
from ...infrastructure.solvers.ode.heun import HeunSolver
from ...infrastructure.solvers.ode.midpoint import MidpointSolver
from ...infrastructure.solvers.ode.runge_kutta4 import RungeKutta4Solver
from ...infrastructure.solvers.ode.verlet import VerletSolver
from ...infrastructure.solvers.pde.explicit_euler_heat import ExplicitEulerHeatSolver
from ...infrastructure.solvers.pde.wave_equation import WaveEquationSolver


class SolverFactory:
    """
    Factory Method that constructs the correct solver from a method identifier.
    Add new solvers here without touching any other layer.
    """

    @classmethod
    def create_integral_solver(cls, method: IntegralMethod) -> IntegralSolverPort:
        match method:
            case IntegralMethod.SIMPSON:
                return SimpsonSolver()
            case IntegralMethod.TRAPEZOIDAL:
                return TrapezoidalSolver()
            case IntegralMethod.MIDPOINT_RECT:
                return MidpointRectSolver()
            case _:
                raise ValueError(f"Unknown integral method: {method!r}")

    @classmethod
    def create_ode_solver(cls, method: ODEMethod) -> ODESolverPort:
        match method:
            case ODEMethod.RUNGE_KUTTA4:
                return RungeKutta4Solver()
            case ODEMethod.HEUN:
                return HeunSolver()
            case ODEMethod.MIDPOINT:
                return MidpointSolver()
            case ODEMethod.VERLET:
                return VerletSolver()
            case _:
                raise ValueError(f"Unknown ODE method: {method!r}")

    @classmethod
    def create_pde_solver(cls, method: PDEMethod) -> PDESolverPort:
        match method:
            case PDEMethod.EXPLICIT_EULER_HEAT:
                return ExplicitEulerHeatSolver()
            case PDEMethod.WAVE_EQUATION:
                return WaveEquationSolver()
            case _:
                raise ValueError(f"Unknown PDE method: {method!r}")
