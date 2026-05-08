from __future__ import annotations

from enum import StrEnum
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ProblemType(StrEnum):
    INTEGRAL = "integral"
    ODE = "ode"
    PDE = "pde"


class IntegralMethod(StrEnum):
    SIMPSON = "simpson"
    TRAPEZOIDAL = "trapezoidal"
    MIDPOINT_RECT = "midpoint_rect"


class ODEMethod(StrEnum):
    RUNGE_KUTTA4 = "runge_kutta4"
    HEUN = "heun"
    MIDPOINT = "midpoint"
    VERLET = "verlet"


class PDEMethod(StrEnum):
    EXPLICIT_EULER_HEAT = "explicit_euler_heat"
    WAVE_EQUATION = "wave_equation"


class VisualizationBackend(StrEnum):
    DISPLAY = "display"
    FILE = "file"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="NM_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    problem_type: ProblemType = Field(default=ProblemType.ODE)
    problem_id: int = Field(default=1, ge=1)

    integral_method: IntegralMethod = Field(default=IntegralMethod.SIMPSON)
    ode_method: ODEMethod = Field(default=ODEMethod.RUNGE_KUTTA4)
    pde_method: PDEMethod = Field(default=PDEMethod.EXPLICIT_EULER_HEAT)

    num_steps: int = Field(default=10000, ge=2)

    visualization_backend: VisualizationBackend = Field(default=VisualizationBackend.FILE)
    output_dir: Path = Field(default=Path("output"))
    figure_dpi: int = Field(default=150, ge=72, le=600)
    figure_format: str = Field(default="png")

    log_level: str = Field(default="INFO")
