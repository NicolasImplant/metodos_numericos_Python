from __future__ import annotations

from ...domain.models.generator_config import GeneratorConfig, GeneratorResult
from ...domain.ports.generator import PseudorandomGeneratorPort
from ._digit_utils import detect_period


class LinearCongruentialGenerator(PseudorandomGeneratorPort):
    """
    Linear Congruential Generator (Lehmer, 1951).

    Recurrence:  x_{n+1} = (a·x_n + c) mod m
    Normalized:  r_n = x_n / (m − 1)

    Hull-Dobell theorem (full period iff):
      1. gcd(c, m) = 1
      2. (a − 1) divisible by every prime factor of m
      3. If 4 | m, then 4 | (a − 1)

    Banks-Carson-Nelson-Nicol conditions (m = 2^g):
      a = 1 + 4k,  c odd,  seed > 0

    Required config fields: seed, count, modulus, multiplier, increment.
    """

    @property
    def method_name(self) -> str:
        return "Congruencial Lineal (Lehmer)"

    def generate(self, config: GeneratorConfig) -> GeneratorResult:
        if config.modulus <= 0:
            raise ValueError("modulus must be > 0")
        if config.increment == 0:
            raise ValueError(
                "increment c must be non-zero for the linear (full-period) variant. "
                "Use MultiplicativeCongruentialGenerator for c = 0."
            )

        m, a, c = config.modulus, config.multiplier, config.increment
        x = config.seed
        seq: list[int] = []
        for _ in range(config.count):
            x = (a * x + c) % m
            seq.append(x)

        t = tuple(seq)
        return GeneratorResult(
            sequence=t,
            normalized=tuple(v / (m - 1) for v in t),
            period=detect_period(t),
            method_name=self.method_name,
            config=config,
        )
