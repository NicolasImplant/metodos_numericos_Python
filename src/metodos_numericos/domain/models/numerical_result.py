from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True)
class IntegralResult:
    area: float
    convergence_history: tuple[float, ...] = field(default_factory=tuple)
    error_history: tuple[float, ...] = field(default_factory=tuple)
    method_name: str = ""
    problem_name: str = ""


@dataclass(frozen=True)
class ODEResult:
    time: NDArray[np.float64]
    states: NDArray[np.float64]
    state_labels: tuple[str, ...]
    method_name: str = ""
    problem_name: str = ""

    def get_state(self, label: str) -> NDArray[np.float64]:
        idx = self.state_labels.index(label)
        return self.states[:, idx]


@dataclass(frozen=True)
class PDEResult:
    spatial_grid: NDArray[np.float64]
    time_grid: NDArray[np.float64]
    solution_matrix: NDArray[np.float64]
    method_name: str = ""
    problem_name: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
