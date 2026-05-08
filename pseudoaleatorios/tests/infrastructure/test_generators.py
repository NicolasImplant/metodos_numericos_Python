"""Generator tests — statistical properties and correctness."""
from __future__ import annotations

import pytest

from pseudoaleatorios.domain.models.generator_config import GeneratorConfig
from pseudoaleatorios.infrastructure.generators.additive_congruential import AdditiveCongruentialGenerator
from pseudoaleatorios.infrastructure.generators.linear_congruential import LinearCongruentialGenerator
from pseudoaleatorios.infrastructure.generators.middle_squares import MiddleSquaresGenerator
from pseudoaleatorios.infrastructure.generators.multiplicative_congruential import MultiplicativeCongruentialGenerator
from pseudoaleatorios.infrastructure.generators.quadratic_congruential import QuadraticCongruentialGenerator
from pseudoaleatorios.infrastructure.analysis.statistics import full_report


class TestLinearCongruentialGenerator:
    def test_all_values_in_unit_interval(self, lcg_config: GeneratorConfig) -> None:
        result = LinearCongruentialGenerator().generate(lcg_config)
        assert all(0.0 <= v < 1.0 for v in result.normalized)

    def test_correct_count(self, lcg_config: GeneratorConfig) -> None:
        result = LinearCongruentialGenerator().generate(lcg_config)
        assert len(result.sequence) == lcg_config.count

    def test_mean_near_half(self, lcg_config: GeneratorConfig) -> None:
        result = LinearCongruentialGenerator().generate(lcg_config)
        assert abs(result.mean - 0.5) < 0.02

    def test_requires_nonzero_increment(self) -> None:
        cfg = GeneratorConfig(seed=1, count=10, modulus=64, multiplier=5, increment=0)
        with pytest.raises(ValueError, match="increment"):
            LinearCongruentialGenerator().generate(cfg)

    def test_method_name(self) -> None:
        assert "Lineal" in LinearCongruentialGenerator().method_name


class TestMultiplicativeCongruentialGenerator:
    def test_all_values_in_unit_interval(self, mcg_config: GeneratorConfig) -> None:
        result = MultiplicativeCongruentialGenerator().generate(mcg_config)
        assert all(0.0 <= v < 1.0 for v in result.normalized)

    def test_rejects_even_seed(self) -> None:
        cfg = GeneratorConfig(seed=1234, count=10, modulus=2**8, multiplier=29)
        with pytest.raises(ValueError, match="odd"):
            MultiplicativeCongruentialGenerator().generate(cfg)

    def test_method_name(self) -> None:
        assert "Multiplicativo" in MultiplicativeCongruentialGenerator().method_name


class TestMiddleSquaresGenerator:
    def test_all_values_in_unit_interval(self, middle_squares_config: GeneratorConfig) -> None:
        result = MiddleSquaresGenerator().generate(middle_squares_config)
        assert all(0.0 <= v < 1.0 for v in result.normalized)

    def test_period_detected_for_degenerate_seed(self) -> None:
        # Seed 0000 → always 0 → period 1
        cfg = GeneratorConfig(seed=100, count=50)
        result = MiddleSquaresGenerator().generate(cfg)
        assert result.period is not None

    def test_method_name(self) -> None:
        assert "Von Neumann" in MiddleSquaresGenerator().method_name


class TestAdditiveCongruentialGenerator:
    def test_all_values_in_unit_interval(self, additive_config: GeneratorConfig) -> None:
        result = AdditiveCongruentialGenerator().generate(additive_config)
        assert all(0.0 <= v < 1.0 for v in result.normalized)

    def test_requires_lag_vector_min_2(self) -> None:
        cfg = GeneratorConfig(seed=0, count=10, modulus=100, lag_vector=(42,))
        with pytest.raises(ValueError, match="lag_vector"):
            AdditiveCongruentialGenerator().generate(cfg)

    def test_method_name(self) -> None:
        assert "Aditivo" in AdditiveCongruentialGenerator().method_name


class TestQuadraticCongruentialGenerator:
    def test_basic_generation(self) -> None:
        cfg = GeneratorConfig(seed=7, count=100, modulus=2**16,
                              coeff_a=3, coeff_b=5, coeff_c=7)
        result = QuadraticCongruentialGenerator().generate(cfg)
        assert len(result.sequence) == 100
        assert all(0.0 <= v < 1.0 for v in result.normalized)

    def test_rejects_bbs_degenerate_case(self) -> None:
        cfg = GeneratorConfig(seed=7, count=10, modulus=64,
                              coeff_a=1, coeff_b=0, coeff_c=0)
        with pytest.raises(ValueError, match="Blum"):
            QuadraticCongruentialGenerator().generate(cfg)


class TestStatisticalReport:
    def test_lcg_passes_chi2(self, lcg_config: GeneratorConfig) -> None:
        result = LinearCongruentialGenerator().generate(lcg_config)
        report = full_report(result.normalized)
        assert report.uniformity.passed, (
            f"Chi2={report.uniformity.statistic:.2f} > {report.uniformity.critical_value}"
        )

    def test_lcg_passes_runs(self, lcg_config: GeneratorConfig) -> None:
        result = LinearCongruentialGenerator().generate(lcg_config)
        report = full_report(result.normalized)
        assert report.runs.passed, f"z={report.runs.z_statistic:.2f}"
