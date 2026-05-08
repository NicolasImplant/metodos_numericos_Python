from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class UniformityTest:
    """Chi-square uniformity test result."""
    statistic: float
    critical_value: float   # α = 0.05, df = bins − 1
    bins: int
    passed: bool
    observed: tuple[int, ...]
    expected_per_bin: float


@dataclass(frozen=True)
class RunsTest:
    """Runs-above/below-mean independence test result."""
    n_runs: int
    expected_runs: float
    std_runs: float
    z_statistic: float
    passed: bool            # |z| < 1.96 at α = 0.05


@dataclass(frozen=True)
class StatisticalReport:
    n: int
    mean: float
    variance: float
    std: float
    minimum: float
    maximum: float
    uniformity: UniformityTest
    runs: RunsTest


# Chi-square critical values at α = 0.05 for df = bins − 1
_CHI2_CRITICAL: dict[int, float] = {
    5:  11.070,
    10: 16.919,
    20: 30.144,
}


def chi_square_uniformity(
    normalized: tuple[float, ...],
    bins: int = 10,
) -> UniformityTest:
    """
    Pearson's chi-square goodness-of-fit test for U[0, 1).

    H₀: the sequence is uniformly distributed on [0, 1).
    Test statistic: χ² = Σ (Oᵢ − E)² / E,  E = n/bins.
    Critical value for α = 0.05 from table (df = bins − 1).
    """
    n = len(normalized)
    expected = n / bins
    observed = [0] * bins
    for v in normalized:
        idx = min(int(v * bins), bins - 1)
        observed[idx] += 1

    stat = sum((o - expected) ** 2 / expected for o in observed)
    critical = _CHI2_CRITICAL.get(bins, _CHI2_CRITICAL[10])

    return UniformityTest(
        statistic=stat,
        critical_value=critical,
        bins=bins,
        passed=stat <= critical,
        observed=tuple(observed),
        expected_per_bin=expected,
    )


def runs_test(normalized: tuple[float, ...]) -> RunsTest:
    """
    Runs-above/below-mean test for independence.

    A "run" is a maximal sequence of values all above or all below the mean.
    Under H₀ (i.i.d. uniform), the expected number of runs and its variance
    are derived from the normal approximation of the runs distribution.
    """
    n = len(normalized)
    mu = sum(normalized) / n
    above = [1 if v >= mu else 0 for v in normalized]

    n1 = sum(above)        # values above mean
    n2 = n - n1            # values below mean

    runs = 1 + sum(1 for i in range(1, n) if above[i] != above[i - 1])

    if n1 == 0 or n2 == 0:
        return RunsTest(n_runs=runs, expected_runs=0.0, std_runs=0.0,
                        z_statistic=0.0, passed=False)

    expected = (2 * n1 * n2) / n + 1
    variance = (2 * n1 * n2 * (2 * n1 * n2 - n)) / (n * n * (n - 1))
    std = math.sqrt(max(variance, 1e-12))
    z = (runs - expected) / std

    return RunsTest(
        n_runs=runs,
        expected_runs=expected,
        std_runs=std,
        z_statistic=z,
        passed=abs(z) <= 1.96,
    )


def full_report(normalized: tuple[float, ...], bins: int = 10) -> StatisticalReport:
    n = len(normalized)
    mu = sum(normalized) / n
    var = sum((x - mu) ** 2 for x in normalized) / n
    return StatisticalReport(
        n=n,
        mean=mu,
        variance=var,
        std=math.sqrt(var),
        minimum=min(normalized),
        maximum=max(normalized),
        uniformity=chi_square_uniformity(normalized, bins),
        runs=runs_test(normalized),
    )
