"""Factory creates the correct concrete generator for each method enum."""
from __future__ import annotations

import pytest

from pseudoaleatorios.application.factories.generator_factory import GeneratorFactory
from pseudoaleatorios.infrastructure.config.settings import GeneratorMethod
from pseudoaleatorios.infrastructure.generators.middle_squares import MiddleSquaresGenerator
from pseudoaleatorios.infrastructure.generators.linear_congruential import LinearCongruentialGenerator
from pseudoaleatorios.infrastructure.generators.multiplicative_congruential import MultiplicativeCongruentialGenerator
from pseudoaleatorios.infrastructure.generators.additive_congruential import AdditiveCongruentialGenerator
from pseudoaleatorios.infrastructure.generators.quadratic_congruential import QuadraticCongruentialGenerator


@pytest.mark.parametrize("method,expected_type", [
    (GeneratorMethod.MIDDLE_SQUARES, MiddleSquaresGenerator),
    (GeneratorMethod.LINEAR_CONGRUENTIAL, LinearCongruentialGenerator),
    (GeneratorMethod.MULTIPLICATIVE_CONGRUENTIAL, MultiplicativeCongruentialGenerator),
    (GeneratorMethod.ADDITIVE_CONGRUENTIAL, AdditiveCongruentialGenerator),
    (GeneratorMethod.QUADRATIC_CONGRUENTIAL, QuadraticCongruentialGenerator),
])
def test_factory_returns_correct_type(method: GeneratorMethod, expected_type: type) -> None:
    generator = GeneratorFactory.create(method)
    assert isinstance(generator, expected_type)


def test_all_methods_registered() -> None:
    for method in GeneratorMethod:
        generator = GeneratorFactory.create(method)
        assert generator.method_name  # non-empty
