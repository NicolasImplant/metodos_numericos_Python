from __future__ import annotations

from abc import ABC, abstractmethod

from ..models.numerical_result import IntegralResult, ODEResult, PDEResult
from ..models.problems import IntegralProblem, ODEProblem, PDEProblem


class IntegralSolverPort(ABC):
    @abstractmethod
    def solve(self, problem: IntegralProblem, n_steps: int) -> IntegralResult: ...

    @property
    @abstractmethod
    def method_name(self) -> str: ...


class ODESolverPort(ABC):
    @abstractmethod
    def solve(self, problem: ODEProblem, n_steps: int) -> ODEResult: ...

    @property
    @abstractmethod
    def method_name(self) -> str: ...


class PDESolverPort(ABC):
    @abstractmethod
    def solve(self, problem: PDEProblem) -> PDEResult: ...

    @property
    @abstractmethod
    def method_name(self) -> str: ...
