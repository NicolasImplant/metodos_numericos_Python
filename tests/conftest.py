from __future__ import annotations

import numpy as np
import pytest

from metodos_numericos.domain.models.problems import IntegralProblem, ODEProblem
from numpy.typing import NDArray


@pytest.fixture()
def sine_integral() -> IntegralProblem:
    return IntegralProblem(
        name="∫₀^π sin(x) dx",
        integrand=lambda x: float(np.sin(x)),
        lower_bound=0.0,
        upper_bound=float(np.pi),
        analytical_value=2.0,
    )


@pytest.fixture()
def semicircle_integral() -> IntegralProblem:
    return IntegralProblem(
        name="∫₋₁¹ √(1-x²) dx",
        integrand=lambda x: float(np.sqrt(max(1 - x**2, 0.0))),
        lower_bound=-1.0,
        upper_bound=1.0,
        analytical_value=float(np.pi / 2),
    )


@pytest.fixture()
def simple_ode() -> ODEProblem:
    """dy/dt = -y  =>  y(t) = e^(-t), analytical solution known."""
    def system(t: float, y: NDArray[np.float64]) -> NDArray[np.float64]:
        return np.array([-y[0]])

    return ODEProblem(
        name="dy/dt = -y (exponential decay)",
        system=system,
        initial_conditions=np.array([1.0]),
        t_start=0.0,
        t_end=5.0,
        state_labels=["y"],
    )
