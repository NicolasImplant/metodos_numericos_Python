from __future__ import annotations

import logging
import sys
from pathlib import Path

from .application.factories.solver_factory import SolverFactory
from .application.use_cases.solve_integral import SolveIntegralUseCase
from .application.use_cases.solve_ode import SolveODEUseCase
from .application.use_cases.solve_pde import SolvePDEUseCase
from .infrastructure.config.settings import ProblemType, Settings
from .infrastructure.visualizers.matplotlib_visualizer import MatplotlibVisualizer


def _configure_logging(level: str) -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt="%H:%M:%S",
    ))
    # Avoid UnicodeEncodeError on Windows cp1252 terminals
    if hasattr(handler.stream, "reconfigure"):
        handler.stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    logging.basicConfig(level=level.upper(), handlers=[handler])


def main() -> None:
    cfg = Settings()
    _configure_logging(cfg.log_level)
    logger = logging.getLogger(__name__)
    logger.info("Config loaded: type=%s id=%d", cfg.problem_type, cfg.problem_id)

    visualizer = MatplotlibVisualizer(
        backend=cfg.visualization_backend,
        dpi=cfg.figure_dpi,
        fmt=cfg.figure_format,
    )

    output_dir = cfg.output_dir
    filename = f"{cfg.problem_type}_p{cfg.problem_id}.{cfg.figure_format}"
    save_path: Path | None = output_dir / filename if cfg.visualization_backend == "file" else None

    match cfg.problem_type:
        case ProblemType.INTEGRAL:
            solver = SolverFactory.create_integral_solver(cfg.integral_method)
            use_case = SolveIntegralUseCase(solver, visualizer)
            result = use_case.execute(cfg.problem_id, cfg.num_steps, save_path)
            print(f"\nResultado: {result.area:.8f}")

        case ProblemType.ODE:
            solver = SolverFactory.create_ode_solver(cfg.ode_method)
            use_case = SolveODEUseCase(solver, visualizer)
            result = use_case.execute(cfg.problem_id, cfg.num_steps, save_path)
            print(f"\nIntegración completa: {result.states.shape[0]} puntos × {result.states.shape[1]} estados")

        case ProblemType.PDE:
            solver = SolverFactory.create_pde_solver(cfg.pde_method)
            use_case = SolvePDEUseCase(solver, visualizer)
            result = use_case.execute(cfg.problem_id, save_path)
            print(f"\nPDE resuelta: malla {result.solution_matrix.shape}")

    if save_path:
        print(f"Gráfica guardada en: {save_path}")


if __name__ == "__main__":
    main()
