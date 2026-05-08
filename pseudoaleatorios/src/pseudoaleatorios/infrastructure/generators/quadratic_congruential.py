from __future__ import annotations

from ...domain.models.generator_config import GeneratorConfig, GeneratorResult
from ...domain.ports.generator import PseudorandomGeneratorPort
from ._digit_utils import detect_period


class QuadraticCongruentialGenerator(PseudorandomGeneratorPort):
    """
    Quadratic Congruential Generator.

    Recurrence:  x_{n+1} = (a·x_n² + b·x_n + c) mod m
    Normalized:  r_n = x_n / (m − 1)

    When a=1, b=0, c=0 the recurrence degenerates to x_{n+1} = x_n² mod m
    (power generator / Blum-Blum-Shub structure); this case raises ValueError
    with guidance to use a dedicated BBS implementation.

    Required config fields: seed, count, modulus, coeff_a, coeff_b, coeff_c.
    """

    @property
    def method_name(self) -> str:
        return "Congruencial Cuadratico"

    def generate(self, config: GeneratorConfig) -> GeneratorResult:
        if config.modulus <= 0:
            raise ValueError("modulus must be > 0")
        if config.coeff_a == 1 and config.coeff_b == 0 and config.coeff_c == 0:
            raise ValueError(
                "With a=1, b=0, c=0 the recurrence reduces to x_{n+1} = x_n^2 mod m "
                "(Blum-Blum-Shub structure). Use a dedicated BBS generator."
            )

        m = config.modulus
        a, b, c = config.coeff_a, config.coeff_b, config.coeff_c
        x = config.seed
        seq: list[int] = []
        for _ in range(config.count):
            x = (a * x * x + b * x + c) % m
            seq.append(x)

        t = tuple(seq)
        return GeneratorResult(
            sequence=t,
            normalized=tuple(v / (m - 1) for v in t),
            period=detect_period(t),
            method_name=self.method_name,
            config=config,
        )
