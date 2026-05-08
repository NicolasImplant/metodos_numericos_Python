from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from ..models.numerical_result import IntegralResult, ODEResult, PDEResult


class VisualizerPort(ABC):
    @abstractmethod
    def plot_integral(self, result: IntegralResult, save_path: Path | None = None) -> None: ...

    @abstractmethod
    def plot_ode(self, result: ODEResult, save_path: Path | None = None) -> None: ...

    @abstractmethod
    def plot_pde(self, result: PDEResult, save_path: Path | None = None) -> None: ...
