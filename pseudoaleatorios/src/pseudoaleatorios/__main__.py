from __future__ import annotations

import logging
import sys

from .application.factories.generator_factory import GeneratorFactory
from .application.use_cases.generate_sequence import GenerateSequenceUseCase
from .domain.models.generator_config import GeneratorConfig
from .infrastructure.config.settings import GeneratorMethod, Settings


def _configure_logging(level: str) -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt="%H:%M:%S",
    ))
    if hasattr(handler.stream, "reconfigure"):
        handler.stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    logging.basicConfig(level=level.upper(), handlers=[handler])


def _build_config(cfg: Settings) -> GeneratorConfig:
    return GeneratorConfig(
        seed=cfg.seed,
        count=cfg.count,
        modulus=cfg.modulus,
        multiplier=cfg.multiplier,
        increment=cfg.increment,
        coeff_a=cfg.coeff_a,
        coeff_b=cfg.coeff_b,
        coeff_c=cfg.coeff_c,
        lag_vector=cfg.lag_vector,
    )


def main() -> None:
    cfg = Settings()
    _configure_logging(cfg.log_level)
    logger = logging.getLogger(__name__)
    logger.info("Config: method=%s  seed=%d  count=%d", cfg.method, cfg.seed, cfg.count)

    generator = GeneratorFactory.create(cfg.method)
    use_case = GenerateSequenceUseCase(generator)
    config = _build_config(cfg)

    result, report = use_case.execute(config, run_statistics=cfg.run_statistics)

    print(f"\n{'='*60}")
    print(f"  Metodo:  {result.method_name}")
    print(f"  Valores: {result.config.count}")
    print(f"  Periodo: {result.period if result.period else 'No detectado'}")
    print(f"  Primeros 10: {list(result.normalized[:10])}")

    if report:
        u = report.uniformity
        r = report.runs
        print(f"\n  --- Estadisticas ---")
        print(f"  Media:    {report.mean:.6f}  (esperada ~0.5)")
        print(f"  Desv.est: {report.std:.6f}  (esperada ~0.2887)")
        print(f"  Chi2:     {u.statistic:.3f}  (critico {u.critical_value:.3f}) -> {'PASA' if u.passed else 'FALLA'}")
        print(f"  Rachas z: {r.z_statistic:.3f}              -> {'PASA' if r.passed else 'FALLA'}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
