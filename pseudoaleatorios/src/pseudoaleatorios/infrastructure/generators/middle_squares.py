from __future__ import annotations

from ...domain.models.generator_config import GeneratorConfig, GeneratorResult
from ...domain.ports.generator import PseudorandomGeneratorPort
from ._digit_utils import detect_period, middle_extract

_MODULUS = 10_000


class MiddleSquaresGenerator(PseudorandomGeneratorPort):
    """
    Von Neumann's middle-squares method (1946).

    Algorithm:
        x_{n+1} = middle_4_digits(x_n²)
        r_n     = x_{n+1} / 10⁴

    Requires: 4-digit seed (1000 ≤ seed ≤ 9999).
    Known weakness: short periods and degenerate fixed points (e.g. x=0).
    """

    @property
    def method_name(self) -> str:
        return "Cuadrados Medios (Von Neumann)"

    def generate(self, config: GeneratorConfig) -> GeneratorResult:
        x = config.seed
        seq: list[int] = []
        for _ in range(config.count):
            x = middle_extract(x * x, pad_to=8, take=4)
            seq.append(x)

        t = tuple(seq)
        return GeneratorResult(
            sequence=t,
            normalized=tuple(v / _MODULUS for v in t),
            period=detect_period(t),
            method_name=self.method_name,
            config=config,
        )
