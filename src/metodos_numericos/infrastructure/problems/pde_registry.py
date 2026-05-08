from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from ...domain.models.problems import PDEProblem


def _heat_ic_1(x: NDArray[np.float64]) -> NDArray[np.float64]:
    L = x[-1]
    return np.array([6 * np.sin(np.pi * xi * (xi + 1e-9) / L) for xi in x])


def _heat_ic_2(x: NDArray[np.float64]) -> NDArray[np.float64]:
    L = x[-1]
    return np.array([np.sin(np.pi * xi * (xi + 1e-9) / L) for xi in x])


def _wave_ic(x: NDArray[np.float64]) -> NDArray[np.float64]:
    L = x[-1]
    return np.sin(np.pi * x / L)


PDE_PROBLEMS: dict[int, PDEProblem] = {
    1: PDEProblem(
        name="Ecuación de difusión de calor (extremos fijos)",
        spatial_length=20.0,
        total_time=1000.0,
        num_spatial_points=50,
        num_time_steps=900,
        diffusivity=0.05,
        initial_condition=_heat_ic_1,
    ),
    2: PDEProblem(
        name="Difusión de calor en una barra (extremo libre)",
        spatial_length=10.0,
        total_time=1000.0,
        num_spatial_points=50,
        num_time_steps=900,
        diffusivity=0.01,
        initial_condition=_heat_ic_2,
    ),
    3: PDEProblem(
        name="Ecuación de onda — cuerda de extremos fijos",
        spatial_length=10.0,
        total_time=1000.0,
        num_spatial_points=50,
        num_time_steps=900,
        diffusivity=0.0,
        wave_speed=0.1,
        initial_condition=_wave_ic,
    ),
    4: PDEProblem(
        name="Ecuación de onda — cuerda con un extremo libre",
        spatial_length=10.0,
        total_time=1000.0,
        num_spatial_points=50,
        num_time_steps=900,
        diffusivity=0.0,
        wave_speed=0.1,
        initial_condition=_wave_ic,
    ),
    5: PDEProblem(
        name="Ecuación de onda — cuerda oscilante extremos fijos",
        spatial_length=10.0,
        total_time=1000.0,
        num_spatial_points=50,
        num_time_steps=900,
        diffusivity=0.0,
        wave_speed=0.1,
        initial_condition=_wave_ic,
    ),
}
