from __future__ import annotations

from ...domain.ports.generator import PseudorandomGeneratorPort
from ...infrastructure.config.settings import GeneratorMethod
from ...infrastructure.generators.additive_congruential import AdditiveCongruentialGenerator
from ...infrastructure.generators.constant_multiplier import ConstantMultiplierGenerator
from ...infrastructure.generators.linear_congruential import LinearCongruentialGenerator
from ...infrastructure.generators.middle_products import MiddleProductsGenerator
from ...infrastructure.generators.middle_squares import MiddleSquaresGenerator
from ...infrastructure.generators.multiplicative_congruential import MultiplicativeCongruentialGenerator
from ...infrastructure.generators.quadratic_congruential import QuadraticCongruentialGenerator


class GeneratorFactory:
    """
    Factory Method: maps a GeneratorMethod enum to the corresponding
    concrete PseudorandomGeneratorPort implementation.
    Adding a new generator requires only a new class + one match branch here.
    """

    @classmethod
    def create(cls, method: GeneratorMethod) -> PseudorandomGeneratorPort:
        match method:
            case GeneratorMethod.MIDDLE_SQUARES:
                return MiddleSquaresGenerator()
            case GeneratorMethod.CONSTANT_MULTIPLIER:
                return ConstantMultiplierGenerator()
            case GeneratorMethod.MIDDLE_PRODUCTS:
                return MiddleProductsGenerator()
            case GeneratorMethod.LINEAR_CONGRUENTIAL:
                return LinearCongruentialGenerator()
            case GeneratorMethod.MULTIPLICATIVE_CONGRUENTIAL:
                return MultiplicativeCongruentialGenerator()
            case GeneratorMethod.ADDITIVE_CONGRUENTIAL:
                return AdditiveCongruentialGenerator()
            case GeneratorMethod.QUADRATIC_CONGRUENTIAL:
                return QuadraticCongruentialGenerator()
            case _:
                raise ValueError(f"Unknown generator method: {method!r}")
