from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import numpy as np
from numpy.typing import NDArray

ODESystem = Callable[[float, NDArray[np.float64]], NDArray[np.float64]]


@dataclass
class IntegralProblem:
    name: str
    integrand: Callable[[float], float] = field(repr=False, compare=False)
    lower_bound: float
    upper_bound: float
    analytical_value: float | None = None


@dataclass
class ODEProblem:
    name: str
    system: ODESystem = field(repr=False, compare=False)
    initial_conditions: NDArray[np.float64] = field(repr=False, compare=False)
    t_start: float
    t_end: float
    state_labels: list[str] = field(default_factory=list)


@dataclass
class PDEProblem:
    name: str
    spatial_length: float
    total_time: float
    num_spatial_points: int
    num_time_steps: int
    diffusivity: float
    wave_speed: float = 0.0
    initial_condition: Callable[[NDArray[np.float64]], NDArray[np.float64]] = field(
        repr=False,
        compare=False,
        default=lambda x: np.zeros_like(x),
    )
    boundary_conditions: tuple[float, float] = (0.0, 0.0)
