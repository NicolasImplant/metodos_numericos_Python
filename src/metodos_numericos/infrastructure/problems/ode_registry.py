from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from ...domain.models.problems import ODEProblem


def _lotka_volterra(t: float, y: NDArray[np.float64]) -> NDArray[np.float64]:
    x, prey_y = y[0], y[1]
    return np.array([3 * x - x * prey_y, x * prey_y - 2 * prey_y])


def _sir(t: float, y: NDArray[np.float64]) -> NDArray[np.float64]:
    i, s = y[0], y[1]
    beta = 0.001407
    return np.array([-0.6 * i + beta * s * i, -beta * s * i, 0.6 * i])


def _lorenz(t: float, y: NDArray[np.float64]) -> NDArray[np.float64]:
    x, lz_y, z = y[0], y[1], y[2]
    return np.array([10.0 * (lz_y - x), x * (27.0 - z) - lz_y, x * lz_y - (8.0 / 3.0) * z])


def _van_der_pol(t: float, y: NDArray[np.float64]) -> NDArray[np.float64]:
    x, v = y[0], y[1]
    mu = 8.53
    A = 1.2
    omega = 2.0 * np.pi / 10.0
    dxdt = v
    dvdt = A * np.sin(omega * t) - x + mu * (1 - x**2) * v
    return np.array([dxdt, dvdt])


def _jerk(t: float, y: NDArray[np.float64]) -> NDArray[np.float64]:
    x, v, a = y[0], y[1], y[2]
    A = 3.6
    return np.array([v, a, x * v**2 - x**3 - A * a])


def _sird(t: float, y: NDArray[np.float64]) -> NDArray[np.float64]:
    s, i = y[0], y[1]
    beta, gamma, mu = 0.4, 0.035, 0.005
    N = s + i
    n_safe = N if N > 0 else 1e-9
    return np.array([
        -beta * s * i / n_safe,
        beta * s * i / n_safe - (gamma + mu) * i,
        gamma * i,
        mu * i,
    ])


def _pendulum_free(t: float, y: NDArray[np.float64]) -> NDArray[np.float64]:
    theta, omega = y[0], y[1]
    g, l = 9.81, 2.0
    return np.array([omega, -(g / l) * np.sin(theta)])


def _pendulum_friction(t: float, y: NDArray[np.float64]) -> NDArray[np.float64]:
    theta, omega = y[0], y[1]
    g, l, k, m = 9.81, 2.0, 0.9, 4.0
    return np.array([omega, -(g / l) * np.sin(theta) - (k / m) * omega])


def _double_pendulum(t: float, y: NDArray[np.float64]) -> NDArray[np.float64]:
    """
    Double pendulum equations of motion derived from the Euler-Lagrange equations.

    State:  y = [theta_1, theta_2, omega_1, omega_2]
    Returns:    [omega_1, omega_2, alpha_1, alpha_2]

    Parameters: m1=m2=1 kg, L1=L2=1 m, g=9.81 m/s^2.

    Denominador: denom = 2*m1 + m2 - m2*cos(2*(theta1 - theta2))
    """
    theta1, theta2, omega1, omega2 = y[0], y[1], y[2], y[3]
    m1, m2, L1, L2, g = 1.0, 1.0, 1.0, 1.0, 9.81
    delta = theta1 - theta2
    denom = 2.0 * m1 + m2 - m2 * np.cos(2.0 * delta)

    alpha1 = (
        -g * (2.0 * m1 + m2) * np.sin(theta1)
        - m2 * g * np.sin(theta1 - 2.0 * theta2)
        - 2.0 * np.sin(delta) * m2 * (omega2**2 * L2 + omega1**2 * L1 * np.cos(delta))
    ) / (L1 * denom)

    alpha2 = (
        2.0
        * np.sin(delta)
        * (
            omega1**2 * L1 * (m1 + m2)
            + g * (m1 + m2) * np.cos(theta1)
            + omega2**2 * L2 * m2 * np.cos(delta)
        )
    ) / (L2 * denom)

    return np.array([omega1, omega2, alpha1, alpha2])


ODE_PROBLEMS: dict[int, ODEProblem] = {
    1: ODEProblem(
        name="Lotka-Volterra (cazador-presa) — RK4",
        system=_lotka_volterra,
        initial_conditions=np.array([1.0, 2.0]),
        t_start=0.0,
        t_end=20.0,
        state_labels=["x (presa)", "y (depredador)"],
    ),
    2: ODEProblem(
        name="Modelo SIR epidemiológico — Heun",
        system=_sir,
        initial_conditions=np.array([5.0, 995.0, 0.0]),
        t_start=0.0,
        t_end=24.0,
        state_labels=["I (infectados)", "S (susceptibles)", "R (recuperados)"],
    ),
    3: ODEProblem(
        name="Atractor de Lorenz — Punto Medio",
        system=_lorenz,
        initial_conditions=np.array([1.0, 0.0, 0.0]),
        t_start=0.0,
        t_end=50.0,
        state_labels=["x", "y", "z"],
    ),
    4: ODEProblem(
        name="Oscilador de Van der Pol (forzado) — RK4",
        system=_van_der_pol,
        initial_conditions=np.array([0.5, 0.0]),
        t_start=0.0,
        t_end=100.0,
        state_labels=["x", "dx/dt"],
    ),
    5: ODEProblem(
        name="Ecuación de Jerk (caótica) — Punto Medio",
        system=_jerk,
        initial_conditions=np.array([0.0, 0.0, 1.0]),
        t_start=0.0,
        t_end=200.0,
        state_labels=["x", "dx/dt", "d²x/dt²"],
    ),
    6: ODEProblem(
        name="Modelo SIRD epidemiológico — Heun",
        system=_sird,
        initial_conditions=np.array([997.0, 3.0, 0.0, 0.0]),
        t_start=0.0,
        t_end=100.0,
        state_labels=["S (susceptibles)", "I (infectados)", "R (recuperados)", "D (fallecidos)"],
    ),
    7: ODEProblem(
        name="Péndulo simple libre — Verlet",
        system=_pendulum_free,
        initial_conditions=np.array([0.5, 0.5]),
        t_start=0.0,
        t_end=10.0,
        state_labels=["θ (posición angular)", "ω (velocidad angular)"],
    ),
    8: ODEProblem(
        name="Péndulo doble caótico — Velocity Verlet",
        system=_double_pendulum,
        initial_conditions=np.array([np.pi / 2, np.pi / 2, 0.0, 0.0]),
        t_start=0.0,
        t_end=30.0,
        state_labels=["θ₁", "θ₂", "ω₁", "ω₂"],
    ),
}
