from __future__ import annotations

from abc import ABC, abstractmethod

from ..models.generator_config import GeneratorConfig, GeneratorResult


class PseudorandomGeneratorPort(ABC):

    @abstractmethod
    def generate(self, config: GeneratorConfig) -> GeneratorResult: ...

    @property
    @abstractmethod
    def method_name(self) -> str: ...
