from __future__ import annotations

import numpy as np

from ...domain.models.problems import IntegralProblem

INTEGRAL_PROBLEMS: dict[int, IntegralProblem] = {
    1: IntegralProblem(
        name="∫₀⁴⁰ e^(-x/3)·cos(x) dx",
        integrand=lambda x: float(np.exp(-x / 3) * np.cos(x)),
        lower_bound=0.0,
        upper_bound=40.0,
    ),
    2: IntegralProblem(
        name="∫₋₁¹ √(1-x²) dx  [= π/2]",
        integrand=lambda x: float(np.sqrt(max(1 - x**2, 0.0))),
        lower_bound=-1.0,
        upper_bound=1.0,
        analytical_value=float(np.pi / 2),
    ),
    3: IntegralProblem(
        name="∫₀¹⁰⁰ sin(x²)/x dx  (Fresnel-type)",
        integrand=lambda x: float(np.sin(x**2) / x) if x != 0.0 else 0.0,
        lower_bound=1e-6,
        upper_bound=100.0,
    ),
    4: IntegralProblem(
        name="∫₀^π sin(x) dx  [= 2]",
        integrand=lambda x: float(np.sin(x)),
        lower_bound=0.0,
        upper_bound=float(np.pi),
        analytical_value=2.0,
    ),
    5: IntegralProblem(
        name="∫₋π/₂^π/₂ log(cos(x)) dx",
        integrand=lambda x: float(np.log(np.cos(x))) if abs(x) < np.pi / 2 - 1e-9 else 0.0,
        lower_bound=-float(np.pi) / 2 + 1e-9,
        upper_bound=float(np.pi) / 2 - 1e-9,
    ),
}
