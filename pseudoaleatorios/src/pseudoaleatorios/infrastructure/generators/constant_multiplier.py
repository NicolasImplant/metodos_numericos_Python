from __future__ import annotations

import random

from ...domain.models.generator_config import GeneratorConfig, GeneratorResult
from ...domain.ports.generator import PseudorandomGeneratorPort
from ._digit_utils import detect_period, middle_extract, sieve_of_eratosthenes

_MODULUS = 10_000
_PRIMES_4D: list[int] = sieve_of_eratosthenes(1000, 9999)


class ConstantMultiplierGenerator(PseudorandomGeneratorPort):
    """
    Constant-multiplier middle-digits method.

    Algorithm:
        x_{n+1} = middle_4_digits(mult × x_n)
        r_n     = x_{n+1} / 10⁴

    `config.multiplier` should be a 4-digit prime for best dispersion.
    If config.multiplier == 0 a random 4-digit prime is chosen automatically.
    """

    @property
    def method_name(self) -> str:
        return "Multiplicador Constante"

    def generate(self, config: GeneratorConfig) -> GeneratorResult:
        mult = config.multiplier or random.choice(_PRIMES_4D)
        x = config.seed
        seq: list[int] = []
        for _ in range(config.count):
            x = middle_extract(mult * x, pad_to=8, take=4)
            seq.append(x)

        t = tuple(seq)
        return GeneratorResult(
            sequence=t,
            normalized=tuple(v / _MODULUS for v in t),
            period=detect_period(t),
            method_name=self.method_name,
            config=config,
        )
