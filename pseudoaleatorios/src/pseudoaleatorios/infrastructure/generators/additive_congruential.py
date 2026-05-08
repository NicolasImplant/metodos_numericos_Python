from __future__ import annotations

from ...domain.models.generator_config import GeneratorConfig, GeneratorResult
from ...domain.ports.generator import PseudorandomGeneratorPort
from ._digit_utils import detect_period


class AdditiveCongruentialGenerator(PseudorandomGeneratorPort):
    """
    Additive Congruential Generator (Lagged Fibonacci Generator).

    Recurrence:  x_{n+1} = (x_n + x_{n−lag+1}) mod m
    where lag = len(config.lag_vector).

    Normalized:  r_n = x_n / (m − 1)

    The initial lag_vector provides the seed values x₀, …, x_{lag−1}.
    Long lags produce long periods; (p, q) pairs (603, 1) and (521, 32)
    are popular choices in practice.

    Required config fields: count, modulus, lag_vector (len ≥ 2).
    """

    @property
    def method_name(self) -> str:
        return "Congruencial Aditivo (Fibonacci Retrasado)"

    def generate(self, config: GeneratorConfig) -> GeneratorResult:
        if len(config.lag_vector) < 2:
            raise ValueError("lag_vector must have at least 2 elements.")
        if config.modulus <= 0:
            raise ValueError("modulus must be > 0")

        m = config.modulus
        lag = len(config.lag_vector)
        buf: list[int] = list(config.lag_vector)
        seq: list[int] = []

        for _ in range(config.count):
            x_next = (buf[-1] + buf[-lag]) % m
            seq.append(x_next)
            buf.append(x_next)

        t = tuple(seq)
        return GeneratorResult(
            sequence=t,
            normalized=tuple(v / (m - 1) for v in t),
            period=detect_period(t),
            method_name=self.method_name,
            config=config,
        )
