from __future__ import annotations

import logging
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from ...domain.models.numerical_result import IntegralResult, ODEResult, PDEResult
from ...domain.ports.visualizer import VisualizerPort

logger = logging.getLogger(__name__)


class MatplotlibVisualizer(VisualizerPort):
    def __init__(self, backend: str = "file", dpi: int = 150, fmt: str = "png") -> None:
        self._backend = backend
        self._dpi = dpi
        self._fmt = fmt
        if backend == "file":
            matplotlib.use("Agg")

    def _show_or_save(self, fig: matplotlib.figure.Figure, save_path: Path | None) -> None:
        if self._backend == "file" and save_path is not None:
            save_path.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(save_path, dpi=self._dpi, format=self._fmt, bbox_inches="tight")
            logger.info("Plot saved -> %s", save_path)
        else:
            plt.show()
        plt.close(fig)

    def plot_integral(self, result: IntegralResult, save_path: Path | None = None) -> None:
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        fig.suptitle(f"{result.problem_name}\nMétodo: {result.method_name}", fontsize=12)

        ax1 = axes[0]
        ax1.plot(result.convergence_history, "b-", linewidth=1.5, label="Área estimada")
        ax1.axhline(result.area, color="red", linestyle="--", linewidth=1, label=f"Final: {result.area:.6f}")
        ax1.set_xlabel("Iteraciones")
        ax1.set_ylabel("Área")
        ax1.set_title("Convergencia")
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        ax2 = axes[1]
        ax2.semilogy(result.error_history, "r-", linewidth=1.5, label="Error relativo")
        ax2.set_xlabel("Iteraciones")
        ax2.set_ylabel("Error relativo")
        ax2.set_title("Error de convergencia")
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        self._show_or_save(fig, save_path)

    def plot_ode(self, result: ODEResult, save_path: Path | None = None) -> None:
        if "x2" in result.metadata:
            self._plot_double_pendulum(result, save_path)
            return
        n_states = result.states.shape[1]
        cols = min(n_states, 3)
        rows = (n_states + cols - 1) // cols + 1  # extra row for phase portrait

        fig = plt.figure(figsize=(6 * cols, 4 * rows))
        fig.suptitle(f"{result.problem_name}\nMétodo: {result.method_name}", fontsize=12)

        colors = plt.cm.tab10.colors  # type: ignore[attr-defined]
        for i, label in enumerate(result.state_labels):
            ax = fig.add_subplot(rows, cols, i + 1)
            ax.plot(result.time, result.states[:, i], color=colors[i % 10], linewidth=1.2, label=label)
            ax.set_xlabel("Tiempo")
            ax.set_ylabel(label)
            ax.set_title(label)
            ax.grid(True, alpha=0.3)
            ax.legend(fontsize=8)

        if n_states >= 2:
            ax_phase = fig.add_subplot(rows, cols, n_states + 1)
            ax_phase.plot(result.states[:, 0], result.states[:, 1], "k-", linewidth=0.6, alpha=0.7)
            ax_phase.set_xlabel(result.state_labels[0])
            ax_phase.set_ylabel(result.state_labels[1])
            ax_phase.set_title("Retrato de fase")
            ax_phase.grid(True, alpha=0.3)

        if n_states == 3:
            ax_3d = fig.add_subplot(rows, cols, n_states + 2, projection="3d")
            ax_3d.plot(result.states[:, 0], result.states[:, 1], result.states[:, 2],
                       linewidth=0.4, alpha=0.8)
            ax_3d.set_xlabel(result.state_labels[0])
            ax_3d.set_ylabel(result.state_labels[1])
            ax_3d.set_zlabel(result.state_labels[2])  # type: ignore[attr-defined]
            ax_3d.set_title("Espacio de fases 3D")

        fig.tight_layout()
        self._show_or_save(fig, save_path)

    def _plot_double_pendulum(self, result: ODEResult, save_path: Path | None = None) -> None:
        meta = result.metadata
        x2, y2 = meta["x2"], meta["y2"]
        energy = meta["energy"]
        t = result.time
        th1, th2 = result.states[:, 0], result.states[:, 1]
        om1, om2 = result.states[:, 2], result.states[:, 3]

        fig = plt.figure(figsize=(16, 10))
        fig.suptitle(f"{result.problem_name}\nMétodo: {result.method_name}", fontsize=12)

        # Trajectory of bob 2 (Cartesian)
        ax_traj = fig.add_subplot(2, 3, 1)
        ax_traj.plot(x2, y2, "b-", linewidth=0.4, alpha=0.7)
        ax_traj.set_xlabel("x₂ (m)")
        ax_traj.set_ylabel("y₂ (m)")
        ax_traj.set_title("Trayectoria del segundo bob")
        ax_traj.set_aspect("equal")
        ax_traj.grid(True, alpha=0.3)

        # Angular positions vs time
        ax_ang = fig.add_subplot(2, 3, 2)
        ax_ang.plot(t, th1, "b-", linewidth=0.8, label="θ₁", alpha=0.85)
        ax_ang.plot(t, th2, "r-", linewidth=0.8, label="θ₂", alpha=0.85)
        ax_ang.set_xlabel("Tiempo (s)")
        ax_ang.set_ylabel("Ángulo (rad)")
        ax_ang.set_title("Posiciones angulares")
        ax_ang.legend(fontsize=8)
        ax_ang.grid(True, alpha=0.3)

        # Energy conservation
        ax_energy = fig.add_subplot(2, 3, 3)
        e0 = energy[0]
        rel_drift = (energy - e0) / abs(e0) if abs(e0) > 1e-12 else energy - e0
        ax_energy.plot(t, rel_drift, "g-", linewidth=0.8)
        ax_energy.set_xlabel("Tiempo (s)")
        ax_energy.set_ylabel("ΔE / E₀")
        ax_energy.set_title("Deriva de energía (conservación)")
        ax_energy.grid(True, alpha=0.3)

        # Phase portrait θ₁ vs ω₁
        ax_ph1 = fig.add_subplot(2, 3, 4)
        ax_ph1.plot(th1, om1, "b-", linewidth=0.4, alpha=0.7)
        ax_ph1.set_xlabel("θ₁ (rad)")
        ax_ph1.set_ylabel("ω₁ (rad/s)")
        ax_ph1.set_title("Retrato de fase — péndulo 1")
        ax_ph1.grid(True, alpha=0.3)

        # Phase portrait θ₂ vs ω₂
        ax_ph2 = fig.add_subplot(2, 3, 5)
        ax_ph2.plot(th2, om2, "r-", linewidth=0.4, alpha=0.7)
        ax_ph2.set_xlabel("θ₂ (rad)")
        ax_ph2.set_ylabel("ω₂ (rad/s)")
        ax_ph2.set_title("Retrato de fase — péndulo 2")
        ax_ph2.grid(True, alpha=0.3)

        # Poincaré-style: ω₁ vs ω₂
        ax_om = fig.add_subplot(2, 3, 6)
        ax_om.plot(om1, om2, "k-", linewidth=0.3, alpha=0.5)
        ax_om.set_xlabel("ω₁ (rad/s)")
        ax_om.set_ylabel("ω₂ (rad/s)")
        ax_om.set_title("Velocidades angulares (ω₁ vs ω₂)")
        ax_om.grid(True, alpha=0.3)

        fig.tight_layout()
        self._show_or_save(fig, save_path)

    def plot_pde(self, result: PDEResult, save_path: Path | None = None) -> None:
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        fig.suptitle(f"{result.problem_name}\nMétodo: {result.method_name}", fontsize=12)

        ax1 = axes[0]
        n_frames = result.solution_matrix.shape[0]
        sample_frames = np.linspace(0, n_frames - 1, min(8, n_frames), dtype=int)
        cmap = plt.cm.viridis  # type: ignore[attr-defined]
        for idx, frame in enumerate(sample_frames):
            color = cmap(idx / max(len(sample_frames) - 1, 1))
            t_val = result.time_grid[frame]
            ax1.plot(result.spatial_grid, result.solution_matrix[frame, :],
                     color=color, linewidth=1.2, label=f"t={t_val:.1f}", alpha=0.8)
        ax1.set_xlabel("x")
        ax1.set_ylabel("u(x, t)")
        ax1.set_title("Evolución temporal (muestras)")
        ax1.legend(fontsize=7)
        ax1.grid(True, alpha=0.3)

        ax2 = axes[1]
        im = ax2.imshow(
            result.solution_matrix.T,
            aspect="auto",
            origin="lower",
            extent=[result.time_grid[0], result.time_grid[-1],
                    result.spatial_grid[0], result.spatial_grid[-1]],
            cmap="hot",
        )
        fig.colorbar(im, ax=ax2, label="u(x, t)")
        ax2.set_xlabel("Tiempo")
        ax2.set_ylabel("x")
        ax2.set_title("Mapa de calor u(x, t)")

        fig.tight_layout()
        self._show_or_save(fig, save_path)
