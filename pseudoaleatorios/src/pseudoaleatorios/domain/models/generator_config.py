from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class GeneratorConfig:
    """
    Unified configuration for all pseudorandom generators.
    Each generator documents which fields it requires.
    """
    seed: int
    count: int
    modulus: int = 0            # m — congruential methods
    multiplier: int = 0         # a — linear / multiplicative congruential
    increment: int = 0          # c — linear congruential (full period)
    coeff_a: int = 0            # a — quadratic: ax² + bx + c
    coeff_b: int = 0            # b — quadratic
    coeff_c: int = 0            # c — quadratic
    lag_vector: tuple[int, ...] = field(default_factory=tuple)  # additive congruential


@dataclass(frozen=True)
class GeneratorResult:
    sequence: tuple[int, ...]
    normalized: tuple[float, ...]   # values in [0, 1)
    period: int | None              # None if no repeat detected within the sequence
    method_name: str
    config: GeneratorConfig

    @property
    def mean(self) -> float:
        return sum(self.normalized) / len(self.normalized)

    @property
    def variance(self) -> float:
        mu = self.mean
        return sum((x - mu) ** 2 for x in self.normalized) / len(self.normalized)

    @property
    def std(self) -> float:
        return self.variance ** 0.5
