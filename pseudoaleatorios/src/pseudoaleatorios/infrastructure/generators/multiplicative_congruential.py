from __future__ import annotations

from ...domain.models.generator_config import GeneratorConfig, GeneratorResult
from ...domain.ports.generator import PseudorandomGeneratorPort
from ._digit_utils import detect_period


class MultiplicativeCongruentialGenerator(PseudorandomGeneratorPort):
    """
    Multiplicative Congruential Generator (special case c = 0).

    Recurrence:  x_{n+1} = a·x_n mod m
    Normalized:  r_n = x_n / (m − 1)

    Maximum period m/4 when m = 2^g and a ≡ 5 (mod 8):
      a = 5 + 8k,  m = 2^g,  seed odd.

    Required config fields: seed (odd), count, modulus (= 2^g), multiplier (= 5 + 8k).
    """

    @property
    def method_name(self) -> str:
        return "Congruencial Multiplicativo"

    def generate(self, config: GeneratorConfig) -> GeneratorResult:
        if config.modulus <= 0:
            raise ValueError("modulus must be > 0")
        if config.seed % 2 == 0:
            raise ValueError(
                "seed must be odd for the multiplicative congruential generator "
                "with m = 2^g to achieve maximum period."
            )

        m, a = config.modulus, config.multiplier
        x = config.seed
        seq: list[int] = []
        for _ in range(config.count):
            x = (a * x) % m
            seq.append(x)

        t = tuple(seq)
        return GeneratorResult(
            sequence=t,
            normalized=tuple(v / (m - 1) for v in t),
            period=detect_period(t),
            method_name=self.method_name,
            config=config,
        )
