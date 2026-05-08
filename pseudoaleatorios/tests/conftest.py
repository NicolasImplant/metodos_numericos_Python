from __future__ import annotations

import pytest

from pseudoaleatorios.domain.models.generator_config import GeneratorConfig


@pytest.fixture()
def lcg_config() -> GeneratorConfig:
    """Hull-Dobell compliant LCG: m=2^31, a=1+4*3=13, c=odd=7."""
    return GeneratorConfig(
        seed=1234,
        count=10_000,
        modulus=2**31,
        multiplier=1_664_525,   # Numerical Recipes classic
        increment=1_013_904_223,
    )


@pytest.fixture()
def mcg_config() -> GeneratorConfig:
    """Multiplicative congruential: m=2^31, a=5+8*3=29 (a≡5 mod 8), odd seed."""
    return GeneratorConfig(
        seed=1235,   # odd
        count=10_000,
        modulus=2**31,
        multiplier=29,
    )


@pytest.fixture()
def middle_squares_config() -> GeneratorConfig:
    return GeneratorConfig(seed=6521, count=200)


@pytest.fixture()
def additive_config() -> GeneratorConfig:
    return GeneratorConfig(
        seed=0,
        count=10_000,
        modulus=100,
        lag_vector=(10, 20, 30, 40, 50),
    )
