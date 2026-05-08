from __future__ import annotations

import random

from ...domain.models.generator_config import GeneratorConfig, GeneratorResult
from ...domain.ports.generator import PseudorandomGeneratorPort
from ._digit_utils import detect_period, middle_extract, sieve_of_eratosthenes

_MODULUS = 10_000
_PRIMES_4D: list[int] = sieve_of_eratosthenes(1000, 9999)


class MiddleProductsGenerator(PseudorandomGeneratorPort):
    """
    Middle-products method (two-seed variant).

    Algorithm:
        x_{n+1} = middle_4_digits(x_n × x_{n-1})
        r_n     = x_{n+1} / 10⁴

    Requires two distinct 4-digit prime seeds:
        config.seed       → x₀
        config.multiplier → x₁  (if 0, a random prime is chosen)
    """

    @property
    def method_name(self) -> str:
        return "Productos Medios"

    def generate(self, config: GeneratorConfig) -> GeneratorResult:
        x_prev = config.seed
        x_curr = config.multiplier or random.choice(_PRIMES_4D)
        seq: list[int] = []
        for _ in range(config.count):
            x_next = middle_extract(x_curr * x_prev, pad_to=8, take=4)
            seq.append(x_next)
            x_prev, x_curr = x_curr, x_next

        t = tuple(seq)
        return GeneratorResult(
            sequence=t,
            normalized=tuple(v / _MODULUS for v in t),
            period=detect_period(t),
            method_name=self.method_name,
            config=config,
        )
